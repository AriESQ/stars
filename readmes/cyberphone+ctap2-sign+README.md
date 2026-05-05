# ctap2-sign

Small Windows command-line program which signs arbitrary clientData 
using FIDO/CTAP2.

## Usage
```
ctap2-sign data2sign domain credentialid
```
`data2sign` holds arbitrary data encoded in Base64Url.<br>
`domain` holds an issuer domain like `test.webpki.org`.<br>
`credentialid` holds the requested credentialId encoded in Base64Url.

The command returns Base64Url encoded values of `signature` and `authenticatorData`.

## FIDO Web Pay
Applied to https://fido-web-pay.github.io/specification/ FIDO/CTAP2
signatures enables CBOR encoded payment authorizations like:

```code
{
  1: "1.0",
  2: {
    1: "Space Shop",
    2: "20220817.0001",
    3: "435.00",
    4: "EUR"
  },
  3: "test.webpki.org",
  4: "FR7630002111110020050014382",
  5: "20500211",
  6: "https://banknet2.org",
  8: {
    1: {
      3: "Windows",
      4: "N/A"
    },
    2: {
      3: "Chrome",
      4: "104"
    }
  },
  9: "2022-08-17T11:24:41+02:00",
  / ENVELOPED SIGNATURE CONTAINER /
  10: {
    / ALGORITHM (COSE) /
    1: -257,
    / PUBLIC KEY (COSE) /
    2: {
      1: 3,
      -1: h'e8e00feae22fdcdaae6de0d71498867e386ca0a6d446e1f24f9169247d92fd3cdd09380471dfbbb98379ba30436c90d6e702a4699ec89e41a1fba0f445b9a01ee1327520bf82c18ac6ec7e811df97d16f281d15e56b676c33faf28eb0b7290947a9d3c895f37b8e9649a1155b3d1ba412b5dd97302f72e758b7092d826f9b07dc03c5417cc912ce60f12e8c268a0e16bebc92b01b558056213676042540b6cdeaba869c0c52eb1e3e9a8a38f19bdcffef12464eb1ac81aac7a6f381075bb507478a0a93e8edff0cdd56903186a33ace1e37c84f30a903b31f5b499cea4798583de2dc511d5bc9fdcb105377f68185af665cca1a957260aee791e55589297f9af',
      -2: h'010001'
    },
    / FIDO AUTHENTICATOR DATA /
    3: h'29a61b658fc4de4d14ce7fbaf1bcd67ec37773fe8b6549118c729a6cdb37b11b0500000005',
    / FIDO SIGNATURE /
    4: h'5326ce0e9ebd7d2ab3dad6da8610d98ef208acd0925d7cbcc3b4b84442908478ba134bbe5f5d1c507acc13beabef86d5fad4982c19d4a4524ac6d7e3aae7ecf2eb7fe202557d4dfb4c20a0dc00066a3860f97718fd12d2e3fa2841ee4ba2bf20d02deacdc3d5e656524000b9fd862310e4066b9696500f14e203e6108540bd9ee0ab430efa15d3af2c7af982193978c55dc5d98a320e84e80d1b8f3c263d32ae155a9b8d06f284c9aad42c81f074e9e7074149dfb4d6f06504e2f61fffdbe6bdc14f939b68c3c22f69aca369b2cb2d83625f91ca37f24780fffafb2d32105f0f7a1a2ef8d2737eac537b1b4893a97d28c0d8a496aa01360dc3ca1e52b7408438'
  }
}
```
That is, the WebAuthn `clientDataJSON` element and associated JSON parsing is _eliminated_.

Although the solution above uses an *enveloped* signature scheme that depends on the
*deterministic mode* of CBOR, nothing prevents you from modifying JOSE
and COSE libraries, to cope with `authenticatorData` the explicit hashing
of `clientData`, and the differing ECDSA signature format.
