# JSON for Classic C++

json.cpp is a baroque JSON parsing / serialization library for C++.

This project is a reaction against <https://github.com/nlohmann/json/>
which provides a modern C++ library for JSON. Our alternative:

- **Goes 2x-3x faster**. With `gcc -O3` 13.2 on Ubuntu 24.04 using an
  AMD Ryzen Threadripper PRO 7995WX this library was able to parse the
  complicated JSON example in [json\_test.cpp](json_test.cpp) 3x faster
  than nlohmann's library.

- **Compiles 10x faster**. An object that does nothing with JSON except
  calling `nlohmann::ordered_json::parse` will take at minimum 1200 ms
  to compile. This is an unacceptably slow minimum overhead. With this
  project, you're instead looking at about 120 ms, and nearly all of
  that overhead is due our dependency on `<string>`, `<map>`, and
  `<vector>`.

- **Has 10x less code**. nlohmann's json.h has 24,766 lines of code. Our
  json.h has 233 lines of code, and our json.cpp file has 1,303 lines.
  This makes our implementation more hackable and easily customizable.
  It's much more restrained when it comes to C++ language feature usage.
  You can easily reason about the behavior of this library and determine
  if it meets the requirements of your production environment.

- **Better JSONTestSuite conformance**. Our JSON parser passes all the
  test cases from <https://github.com/nst/JSONTestSuite/>. However
  nlohmann's json library doesn't fully pass.

To use this library, you need three things. First, you need json.h.
Secondly, you need json.cpp. Thirdly, you need Google's outstanding
double-conversion library.

We like double-conversion because it has a really good method for
serializing 32-bit floating point numbers. This is useful if you're
building something like an HTTP server that serves embeddings. With
other JSON serializers that depend only on the C library and STL, floats
are upcast to double so you'd be sending big ugly arrays like
`[0.2893893899832212, ...]` which doesn't make sense, because most of
those bits are made up, since a float32 can't hold that much precision.
But with this library, the `Json` object will remember that you passed
it a float, and then serialize it as such when you call `toString()`,
thus allowing for more efficient readable responses.

## Benchmark Results

Here are some quick and dirty tests for parsing and serialization. The
lower numbers are better. See [json\_test.cpp](json_test.cpp) and
[nlohmann/json\_test.cpp](nlohmann/json_test.cpp). Please note that the
`json_test_suite()` function was modified locally to only include the
successful test cases, in the hope of controlling for differences in
exception handling. The test, as written, actually reports a 39x (rather
than 3x) advantage, which we haven't figured out how to explain yet.

```
    # json.cpp
        71 ns 2000x object_test()
       226 ns 2000x deep_test()
       675 ns 2000x parse_test()
      1309 ns 2000x round_trip_test()
     10462 ns 2000x json_test_suite()

    # nlohmann::ordered_json
        202 ns 2000x object_test()
        659 ns 2000x deep_test()
       1928 ns 2000x parse_test()
       4258 ns 2000x round_trip_test()
      16617 ns 2000x json_test_suite()
```

## Usage Example

The [llamafile](https://github.com/Mozilla-Ocho/llamafile) project uses
this JSON library. Here are some excerpts from its OpenAI API compatible
`/v1/chat/completions` endpoint.

Here's the code where it parses the incoming HTTP body and validates it.

```cpp
    // object<model, messages, ...>
    auto [status, json] = jt::Json::parse(std::string(payload_));
    if (status != jt::Json::success)
        return send_error(400, jt::Json::StatusToString(status));
    if (!json.isObject())
        return send_error(400, "JSON body must be an object");

    // fields openai documents that we don't support yet
    if (json.contains("tools"))
        return send_error(400, "OpenAI tools field not supported yet");
    if (json.contains("audio"))
        return send_error(400, "OpenAI audio field not supported yet");

    // model: string
    jt::Json& model = json["model"];
    if (!model.isString())
        return send_error(400, "JSON missing model string");
    params->model = model.getString();

    // messages: array<object<role:string, content:string>>
    if (!json["messages"].isArray())
        return send_error(400, "JSON missing messages array");
    std::vector<Json>& messages = json["messages"].getArray();
    if (messages.empty())
        return send_error(400, "JSON messages array is empty");
    for (Json& message : messages) {
        if (!message.isObject())
            return send_error(400, "messages array must hold objects");
        if (!message["role"].isString())
            return send_error(400, "message must have string role");
        if (!is_legal_role(message["role"].getString()))
            return send_error(400, "message role not system user assistant");
        if (!message["content"].isString())
            return send_error(400, "message must have string content");
        params->messages.emplace_back(message["role"].getString(),
                                      message["content"].getString());
    }

    // ...
```

Here's the code where it sends a response.

```cpp
struct V1ChatCompletionResponse
{
    std::string content;
    jt::Json json;
};

bool
Client::v1_chat_completions()
{
    // ...

    V1ChatCompletionResponse* response = new V1ChatCompletionResponse;
    defer_cleanup(cleanup_response, response);

    // ...

    // setup response json
    response->json["id"] = generate_id();
    response->json["object"] = "chat.completion";
    response->json["model"] = params->model;
    response->json["system_fingerprint"] = slot_->system_fingerprint_;
    Json& choice = response->json["choices"][0];
    choice["index"] = 0;
    choice["logprobs"] = nullptr;
    choice["finish_reason"] = nullptr;

    // initialize response
    if (params->stream) {
        char* p = append_http_response_message(obuf_.p, 200);
        p = stpcpy(p, "Content-Type: text/event-stream\r\n");
        if (!send_response_start(obuf_.p, p))
            return false;
        choice["delta"]["role"] = "assistant";
        choice["delta"]["content"] = "";
        response->json["created"] = timespec_real().tv_sec;
        response->content = make_event(response->json);
        choice.getObject().erase("delta");
        if (!send_response_chunk(response->content))
            return false;
    }

    // prediction time
    int completion_tokens = 0;
    const char* finish_reason = "length";
    for (;;) {
        // do token generation ...
    }
    choice["finish_reason"] = finish_reason;

    // finalize response
    cleanup_slot(this);
    if (params->stream) {
        choice["delta"]["content"] = "";
        response->json["created"] = timespec_real().tv_sec;
        response->content = make_event(response->json);
        choice.getObject().erase("delta");
        if (!send_response_chunk(response->content))
            return false;
        return send_response_finish();
    } else {
        Json& usage = response->json["usage"];
        usage["prompt_tokens"] = prompt_tokens;
        usage["completion_tokens"] = completion_tokens;
        usage["total_tokens"] = completion_tokens + prompt_tokens;
        choice["message"]["role"] = "assistant";
        choice["message"]["content"] = std::move(response->content);
        response->json["created"] = timespec_real().tv_sec;
        char* p = append_http_response_message(obuf_.p, 200);
        p = stpcpy(p, "Content-Type: application/json\r\n");
        response->content = response->json.toStringPretty();
        response->content += '\n';
        return send_response(obuf_.p, p, response->content);
    }
```

See also <https://github.com/Mozilla-Ocho/llamafile/blob/main/llamafile/server/v1_chat_completions.cpp>

## JSONTestSuite Results

Here's the results of running `jsontestsuite_test` for json.cpp.

### Undefined test cases

The parser implementation is free to choose to accept or reject.

```
i_number_double_huge_neg_exp.json                                      IMPLEMENTATION_PASS
i_number_huge_exp.json                                                 IMPLEMENTATION_PASS
i_number_neg_int_huge_exp.json                                         IMPLEMENTATION_PASS
i_number_pos_double_huge_exp.json                                      IMPLEMENTATION_PASS
i_number_real_neg_overflow.json                                        IMPLEMENTATION_PASS
i_number_real_pos_overflow.json                                        IMPLEMENTATION_PASS
i_number_real_underflow.json                                           IMPLEMENTATION_PASS
i_number_too_big_neg_int.json                                          IMPLEMENTATION_PASS
i_number_too_big_pos_int.json                                          IMPLEMENTATION_PASS
i_number_very_big_negative_int.json                                    IMPLEMENTATION_PASS
i_object_key_lone_2nd_surrogate.json                                   IMPLEMENTATION_PASS
i_string_1st_surrogate_but_2nd_missing.json                            IMPLEMENTATION_PASS
i_string_1st_valid_surrogate_2nd_invalid.json                          IMPLEMENTATION_PASS
i_string_incomplete_surrogate_and_escape_valid.json                    IMPLEMENTATION_PASS
i_string_incomplete_surrogate_pair.json                                IMPLEMENTATION_PASS
i_string_incomplete_surrogates_escape_valid.json                       IMPLEMENTATION_PASS
i_string_invalid_lonely_surrogate.json                                 IMPLEMENTATION_PASS
i_string_invalid_surrogate.json                                        IMPLEMENTATION_PASS
i_string_invalid_utf-8.json                                            IMPLEMENTATION_FAIL (illegal_utf8_character)
i_string_inverted_surrogates_U+1D11E.json                              IMPLEMENTATION_PASS
i_string_iso_latin_1.json                                              IMPLEMENTATION_FAIL (malformed_utf8)
i_string_lone_second_surrogate.json                                    IMPLEMENTATION_PASS
i_string_lone_utf8_continuation_byte.json                              IMPLEMENTATION_FAIL (c1_control_code_in_string)
i_string_not_in_unicode_range.json                                     IMPLEMENTATION_FAIL (utf8_exceeds_utf16_range)
i_string_overlong_sequence_2_bytes.json                                IMPLEMENTATION_FAIL (overlong_ascii)
i_string_overlong_sequence_6_bytes.json                                IMPLEMENTATION_FAIL (illegal_utf8_character)
i_string_overlong_sequence_6_bytes_null.json                           IMPLEMENTATION_FAIL (illegal_utf8_character)
i_string_truncated-utf-8.json                                          IMPLEMENTATION_FAIL (malformed_utf8)
i_string_utf16BE_no_BOM.json                                           IMPLEMENTATION_FAIL (illegal_character)
i_string_utf16LE_no_BOM.json                                           IMPLEMENTATION_FAIL (illegal_character)
i_string_UTF-16LE_with_BOM.json                                        IMPLEMENTATION_FAIL (illegal_character)
i_string_UTF-8_invalid_sequence.json                                   IMPLEMENTATION_FAIL (illegal_utf8_character)
i_string_UTF8_surrogate_U+D800.json                                    IMPLEMENTATION_FAIL (utf16_surrogate_in_utf8)
i_structure_500_nested_arrays.json                                     IMPLEMENTATION_FAIL (depth_exceeded)
i_structure_UTF-8_BOM_empty_object.json                                IMPLEMENTATION_FAIL (illegal_character)
```

### Invalid JSON test cases

The parser must reject this data.

```
n_array_1_true_without_comma.json                                      REJECTED (missing_comma)
n_array_a_invalid_utf8.json                                            REJECTED (illegal_character)
n_array_colon_instead_of_comma.json                                    REJECTED (unexpected_colon)
n_array_comma_after_close.json                                         REJECTED (trailing_content)
n_array_comma_and_number.json                                          REJECTED (unexpected_comma)
n_array_double_comma.json                                              REJECTED (unexpected_comma)
n_array_double_extra_comma.json                                        REJECTED (unexpected_comma)
n_array_extra_close.json                                               REJECTED (trailing_content)
n_array_extra_comma.json                                               REJECTED (unexpected_end_of_array)
n_array_incomplete_invalid_value.json                                  REJECTED (illegal_character)
n_array_incomplete.json                                                REJECTED (unexpected_eof)
n_array_inner_array_no_comma.json                                      REJECTED (missing_comma)
n_array_invalid_utf8.json                                              REJECTED (illegal_character)
n_array_items_separated_by_semicolon.json                              REJECTED (unexpected_colon)
n_array_just_comma.json                                                REJECTED (unexpected_comma)
n_array_just_minus.json                                                REJECTED (bad_negative)
n_array_missing_value.json                                             REJECTED (unexpected_comma)
n_array_newlines_unclosed.json                                         REJECTED (unexpected_eof)
n_array_number_and_comma.json                                          REJECTED (unexpected_end_of_array)
n_array_number_and_several_commas.json                                 REJECTED (unexpected_comma)
n_array_spaces_vertical_tab_formfeed.json                              REJECTED (non_del_c0_control_code_in_string)
n_array_star_inside.json                                               REJECTED (illegal_character)
n_array_unclosed.json                                                  REJECTED (unexpected_eof)
n_array_unclosed_trailing_comma.json                                   REJECTED (unexpected_eof)
n_array_unclosed_with_new_lines.json                                   REJECTED (unexpected_eof)
n_array_unclosed_with_object_inside.json                               REJECTED (unexpected_eof)
n_incomplete_false.json                                                REJECTED (illegal_character)
n_incomplete_null.json                                                 REJECTED (illegal_character)
n_incomplete_true.json                                                 REJECTED (illegal_character)
n_multidigit_number_then_00.json                                       REJECTED (trailing_content)
n_number_0.1.2.json                                                    REJECTED (illegal_character)
n_number_-01.json                                                      REJECTED (unexpected_octal)
n_number_0.3e+.json                                                    REJECTED (bad_exponent)
n_number_0.3e.json                                                     REJECTED (bad_exponent)
n_number_0_capital_E+.json                                             REJECTED (bad_exponent)
n_number_0_capital_E.json                                              REJECTED (bad_exponent)
n_number_0.e1.json                                                     REJECTED (bad_double)
n_number_0e+.json                                                      REJECTED (bad_exponent)
n_number_0e.json                                                       REJECTED (bad_exponent)
n_number_1_000.json                                                    REJECTED (missing_comma)
n_number_1.0e+.json                                                    REJECTED (bad_exponent)
n_number_1.0e-.json                                                    REJECTED (bad_exponent)
n_number_1.0e.json                                                     REJECTED (bad_exponent)
n_number_-1.0..json                                                    REJECTED (illegal_character)
n_number_1eE2.json                                                     REJECTED (bad_exponent)
n_number_+1.json                                                       REJECTED (illegal_character)
n_number_.-1.json                                                      REJECTED (illegal_character)
n_number_2.e+3.json                                                    REJECTED (bad_double)
n_number_2.e-3.json                                                    REJECTED (bad_double)
n_number_2.e3.json                                                     REJECTED (bad_double)
n_number_.2e-3.json                                                    REJECTED (illegal_character)
n_number_-2..json                                                      REJECTED (bad_double)
n_number_9.e+.json                                                     REJECTED (bad_double)
n_number_expression.json                                               REJECTED (illegal_character)
n_number_hex_1_digit.json                                              REJECTED (illegal_character)
n_number_hex_2_digits.json                                             REJECTED (illegal_character)
n_number_infinity.json                                                 REJECTED (illegal_character)
n_number_+Inf.json                                                     REJECTED (illegal_character)
n_number_Inf.json                                                      REJECTED (illegal_character)
n_number_invalid+-.json                                                REJECTED (bad_exponent)
n_number_invalid-negative-real.json                                    REJECTED (missing_comma)
n_number_invalid-utf-8-in-bigger-int.json                              REJECTED (illegal_character)
n_number_invalid-utf-8-in-exponent.json                                REJECTED (illegal_character)
n_number_invalid-utf-8-in-int.json                                     REJECTED (illegal_character)
n_number_++.json                                                       REJECTED (illegal_character)
n_number_minus_infinity.json                                           REJECTED (bad_negative)
n_number_minus_sign_with_trailing_garbage.json                         REJECTED (bad_negative)
n_number_minus_space_1.json                                            REJECTED (bad_negative)
n_number_-NaN.json                                                     REJECTED (bad_negative)
n_number_NaN.json                                                      REJECTED (illegal_character)
n_number_neg_int_starting_with_zero.json                               REJECTED (unexpected_octal)
n_number_neg_real_without_int_part.json                                REJECTED (bad_negative)
n_number_neg_with_garbage_at_end.json                                  REJECTED (illegal_character)
n_number_real_garbage_after_e.json                                     REJECTED (bad_exponent)
n_number_real_with_invalid_utf8_after_e.json                           REJECTED (bad_exponent)
n_number_real_without_fractional_part.json                             REJECTED (bad_double)
n_number_starting_with_dot.json                                        REJECTED (illegal_character)
n_number_U+FF11_fullwidth_digit_one.json                               REJECTED (illegal_character)
n_number_with_alpha_char.json                                          REJECTED (illegal_character)
n_number_with_alpha.json                                               REJECTED (illegal_character)
n_number_with_leading_zero.json                                        REJECTED (unexpected_octal)
n_object_bad_value.json                                                REJECTED (illegal_character)
n_object_bracket_key.json                                              REJECTED (object_key_must_be_string)
n_object_comma_instead_of_colon.json                                   REJECTED (unexpected_comma)
n_object_double_colon.json                                             REJECTED (unexpected_colon)
n_object_emoji.json                                                    REJECTED (illegal_character)
n_object_garbage_at_end.json                                           REJECTED (object_key_must_be_string)
n_object_key_with_single_quotes.json                                   REJECTED (illegal_character)
n_object_lone_continuation_byte_in_key_and_trailing_comma.json         REJECTED (illegal_utf8_character)
n_object_missing_colon.json                                            REJECTED (illegal_character)
n_object_missing_key.json                                              REJECTED (unexpected_colon)
n_object_missing_semicolon.json                                        REJECTED (missing_colon)
n_object_missing_value.json                                            REJECTED (unexpected_eof)
n_object_no-colon.json                                                 REJECTED (unexpected_eof)
n_object_non_string_key_but_huge_number_instead.json                   REJECTED (object_key_must_be_string)
n_object_non_string_key.json                                           REJECTED (object_key_must_be_string)
n_object_repeated_null_null.json                                       REJECTED (object_key_must_be_string)
n_object_several_trailing_commas.json                                  REJECTED (unexpected_comma)
n_object_single_quote.json                                             REJECTED (illegal_character)
n_object_trailing_comma.json                                           REJECTED (unexpected_end_of_object)
n_object_trailing_comment.json                                         REJECTED (trailing_content)
n_object_trailing_comment_open.json                                    REJECTED (trailing_content)
n_object_trailing_comment_slash_open_incomplete.json                   REJECTED (trailing_content)
n_object_trailing_comment_slash_open.json                              REJECTED (trailing_content)
n_object_two_commas_in_a_row.json                                      REJECTED (unexpected_comma)
n_object_unquoted_key.json                                             REJECTED (illegal_character)
n_object_unterminated-value.json                                       REJECTED (unexpected_end_of_string)
n_object_with_single_string.json                                       REJECTED (unexpected_end_of_object)
n_object_with_trailing_garbage.json                                    REJECTED (trailing_content)
n_single_space.json                                                    REJECTED (absent_value)
n_string_1_surrogate_then_escape.json                                  REJECTED (unexpected_end_of_string)
n_string_1_surrogate_then_escape_u1.json                               REJECTED (invalid_unicode_escape)
n_string_1_surrogate_then_escape_u1x.json                              REJECTED (invalid_unicode_escape)
n_string_1_surrogate_then_escape_u.json                                REJECTED (invalid_unicode_escape)
n_string_accentuated_char_no_quotes.json                               REJECTED (illegal_character)
n_string_backslash_00.json                                             REJECTED (invalid_escape_character)
n_string_escaped_backslash_bad.json                                    REJECTED (unexpected_end_of_string)
n_string_escaped_ctrl_char_tab.json                                    REJECTED (invalid_escape_character)
n_string_escaped_emoji.json                                            REJECTED (invalid_escape_character)
n_string_escape_x.json                                                 REJECTED (hex_escape_not_printable)
n_string_incomplete_escaped_character.json                             REJECTED (invalid_unicode_escape)
n_string_incomplete_escape.json                                        REJECTED (unexpected_end_of_string)
n_string_incomplete_surrogate_escape_invalid.json                      REJECTED (invalid_hex_escape)
n_string_incomplete_surrogate.json                                     REJECTED (invalid_unicode_escape)
n_string_invalid_backslash_esc.json                                    REJECTED (invalid_escape_character)
n_string_invalid_unicode_escape.json                                   REJECTED (invalid_unicode_escape)
n_string_invalid_utf8_after_escape.json                                REJECTED (invalid_escape_character)
n_string_invalid-utf-8-in-escape.json                                  REJECTED (invalid_unicode_escape)
n_string_leading_uescaped_thinspace.json                               REJECTED (illegal_character)
n_string_no_quotes_with_bad_escape.json                                REJECTED (illegal_character)
n_string_single_doublequote.json                                       REJECTED (unexpected_end_of_string)
n_string_single_quote.json                                             REJECTED (illegal_character)
n_string_single_string_no_double_quotes.json                           REJECTED (illegal_character)
n_string_start_escape_unclosed.json                                    REJECTED (unexpected_end_of_string)
n_string_unescaped_ctrl_char.json                                      REJECTED (non_del_c0_control_code_in_string)
n_string_unescaped_newline.json                                        REJECTED (non_del_c0_control_code_in_string)
n_string_unescaped_tab.json                                            REJECTED (non_del_c0_control_code_in_string)
n_string_unicode_CapitalU.json                                         REJECTED (invalid_escape_character)
n_string_with_trailing_garbage.json                                    REJECTED (trailing_content)
n_structure_100000_opening_arrays.json                                 REJECTED (depth_exceeded)
n_structure_angle_bracket_..json                                       REJECTED (illegal_character)
n_structure_angle_bracket_null.json                                    REJECTED (illegal_character)
n_structure_array_trailing_garbage.json                                REJECTED (trailing_content)
n_structure_array_with_extra_array_close.json                          REJECTED (trailing_content)
n_structure_array_with_unclosed_string.json                            REJECTED (unexpected_end_of_string)
n_structure_ascii-unicode-identifier.json                              REJECTED (illegal_character)
n_structure_capitalized_True.json                                      REJECTED (illegal_character)
n_structure_close_unopened_array.json                                  REJECTED (trailing_content)
n_structure_comma_instead_of_closing_brace.json                        REJECTED (unexpected_eof)
n_structure_double_array.json                                          REJECTED (trailing_content)
n_structure_end_array.json                                             REJECTED (unexpected_end_of_array)
n_structure_incomplete_UTF8_BOM.json                                   REJECTED (illegal_character)
n_structure_lone-invalid-utf-8.json                                    REJECTED (illegal_character)
n_structure_lone-open-bracket.json                                     REJECTED (unexpected_eof)
n_structure_no_data.json                                               REJECTED (absent_value)
n_structure_null-byte-outside-string.json                              REJECTED (illegal_character)
n_structure_number_with_trailing_garbage.json                          REJECTED (trailing_content)
n_structure_object_followed_by_closing_object.json                     REJECTED (trailing_content)
n_structure_object_unclosed_no_value.json                              REJECTED (unexpected_eof)
n_structure_object_with_comment.json                                   REJECTED (illegal_character)
n_structure_object_with_trailing_garbage.json                          REJECTED (trailing_content)
n_structure_open_array_apostrophe.json                                 REJECTED (illegal_character)
n_structure_open_array_comma.json                                      REJECTED (unexpected_comma)
n_structure_open_array_object.json                                     REJECTED (depth_exceeded)
n_structure_open_array_open_object.json                                REJECTED (unexpected_eof)
n_structure_open_array_open_string.json                                REJECTED (unexpected_end_of_string)
n_structure_open_array_string.json                                     REJECTED (unexpected_eof)
n_structure_open_object_close_array.json                               REJECTED (unexpected_end_of_array)
n_structure_open_object_comma.json                                     REJECTED (unexpected_comma)
n_structure_open_object.json                                           REJECTED (unexpected_eof)
n_structure_open_object_open_array.json                                REJECTED (object_key_must_be_string)
n_structure_open_object_open_string.json                               REJECTED (unexpected_end_of_string)
n_structure_open_object_string_with_apostrophes.json                   REJECTED (illegal_character)
n_structure_open_open.json                                             REJECTED (invalid_escape_character)
n_structure_single_eacute.json                                         REJECTED (illegal_character)
n_structure_single_star.json                                           REJECTED (illegal_character)
n_structure_trailing_#.json                                            REJECTED (trailing_content)
n_structure_U+2060_word_joined.json                                    REJECTED (illegal_character)
n_structure_uescaped_LF_before_string.json                             REJECTED (illegal_character)
n_structure_unclosed_array.json                                        REJECTED (unexpected_eof)
n_structure_unclosed_array_partial_null.json                           REJECTED (illegal_character)
n_structure_unclosed_array_unfinished_false.json                       REJECTED (illegal_character)
n_structure_unclosed_array_unfinished_true.json                        REJECTED (illegal_character)
n_structure_unclosed_object.json                                       REJECTED (unexpected_eof)
n_structure_unicode-identifier.json                                    REJECTED (illegal_character)
n_structure_UTF8_BOM_no_data.json                                      REJECTED (illegal_character)
n_structure_whitespace_formfeed.json                                   REJECTED (illegal_character)
n_structure_whitespace_U+2060_word_joiner.json                         REJECTED (illegal_character)
```

### Success JSON test cases

The parser must accept this JSON as valid.

```
y_array_arraysWithSpaces.json                                          PASSED
y_array_empty.json                                                     PASSED
y_array_empty-string.json                                              PASSED
y_array_ending_with_newline.json                                       PASSED
y_array_false.json                                                     PASSED
y_array_heterogeneous.json                                             PASSED
y_array_null.json                                                      PASSED
y_array_with_1_and_newline.json                                        PASSED
y_array_with_leading_space.json                                        PASSED
y_array_with_several_null.json                                         PASSED
y_array_with_trailing_space.json                                       PASSED
y_number_0e+1.json                                                     PASSED
y_number_0e1.json                                                      PASSED
y_number_after_space.json                                              PASSED
y_number_double_close_to_zero.json                                     PASSED
y_number_int_with_exp.json                                             PASSED
y_number.json                                                          PASSED
y_number_minus_zero.json                                               PASSED
y_number_negative_int.json                                             PASSED
y_number_negative_one.json                                             PASSED
y_number_negative_zero.json                                            PASSED
y_number_real_capital_e.json                                           PASSED
y_number_real_capital_e_neg_exp.json                                   PASSED
y_number_real_capital_e_pos_exp.json                                   PASSED
y_number_real_exponent.json                                            PASSED
y_number_real_fraction_exponent.json                                   PASSED
y_number_real_neg_exp.json                                             PASSED
y_number_real_pos_exponent.json                                        PASSED
y_number_simple_int.json                                               PASSED
y_number_simple_real.json                                              PASSED
y_object_basic.json                                                    PASSED
y_object_duplicated_key_and_value.json                                 PASSED
y_object_duplicated_key.json                                           PASSED
y_object_empty.json                                                    PASSED
y_object_empty_key.json                                                PASSED
y_object_escaped_null_in_key.json                                      PASSED
y_object_extreme_numbers.json                                          PASSED
y_object.json                                                          PASSED
y_object_long_strings.json                                             PASSED
y_object_simple.json                                                   PASSED
y_object_string_unicode.json                                           PASSED
y_object_with_newlines.json                                            PASSED
y_string_1_2_3_bytes_UTF-8_sequences.json                              PASSED
y_string_accepted_surrogate_pair.json                                  PASSED
y_string_accepted_surrogate_pairs.json                                 PASSED
y_string_allowed_escapes.json                                          PASSED
y_string_backslash_and_u_escaped_zero.json                             PASSED
y_string_backslash_doublequotes.json                                   PASSED
y_string_comments.json                                                 PASSED
y_string_double_escape_a.json                                          PASSED
y_string_double_escape_n.json                                          PASSED
y_string_escaped_control_character.json                                PASSED
y_string_escaped_noncharacter.json                                     PASSED
y_string_in_array.json                                                 PASSED
y_string_in_array_with_leading_space.json                              PASSED
y_string_last_surrogates_1_and_2.json                                  PASSED
y_string_nbsp_uescaped.json                                            PASSED
y_string_nonCharacterInUTF-8_U+10FFFF.json                             PASSED
y_string_nonCharacterInUTF-8_U+FFFF.json                               PASSED
y_string_null_escape.json                                              PASSED
y_string_one-byte-utf-8.json                                           PASSED
y_string_pi.json                                                       PASSED
y_string_reservedCharacterInUTF-8_U+1BFFF.json                         PASSED
y_string_simple_ascii.json                                             PASSED
y_string_space.json                                                    PASSED
y_string_surrogates_U+1D11E_MUSICAL_SYMBOL_G_CLEF.json                 PASSED
y_string_three-byte-utf-8.json                                         PASSED
y_string_two-byte-utf-8.json                                           PASSED
y_string_u+2028_line_sep.json                                          PASSED
y_string_u+2029_par_sep.json                                           PASSED
y_string_uescaped_newline.json                                         PASSED
y_string_uEscape.json                                                  PASSED
y_string_unescaped_char_delete.json                                    PASSED
y_string_unicode_2.json                                                PASSED
y_string_unicodeEscapedBackslash.json                                  PASSED
y_string_unicode_escaped_double_quote.json                             PASSED
y_string_unicode.json                                                  PASSED
y_string_unicode_U+10FFFE_nonchar.json                                 PASSED
y_string_unicode_U+1FFFE_nonchar.json                                  PASSED
y_string_unicode_U+200B_ZERO_WIDTH_SPACE.json                          PASSED
y_string_unicode_U+2064_invisible_plus.json                            PASSED
y_string_unicode_U+FDD0_nonchar.json                                   PASSED
y_string_unicode_U+FFFE_nonchar.json                                   PASSED
y_string_utf8.json                                                     PASSED
y_string_with_del_character.json                                       PASSED
y_structure_lonely_false.json                                          PASSED
y_structure_lonely_int.json                                            PASSED
y_structure_lonely_negative_real.json                                  PASSED
y_structure_lonely_null.json                                           PASSED
y_structure_lonely_string.json                                         PASSED
y_structure_lonely_true.json                                           PASSED
y_structure_string_empty.json                                          PASSED
y_structure_trailing_newline.json                                      PASSED
y_structure_true_in_array.json                                         PASSED
y_structure_whitespace_array.json                                      PASSED
```

## History

This JSON parser was coded in 2022 by Justine Tunney and Gautham
Venkatasubramanian. It was originally written in C for Lua in
[Redbean](https://redbean.dev). See
<https://github.com/jart/cosmopolitan/blob/master/tool/net/ljson.c> for
the original source code. In 2024 Mozilla sponsored converting the
Redbean JSON library to C++ for
[llamafile](https://github.com/Mozilla-Ocho/llamafile).
