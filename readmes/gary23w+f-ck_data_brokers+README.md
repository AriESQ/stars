# f*ck_data_brokers.py

"Today was funny: I was dealing with some scumbag data broker this morning, trying to get a
good friend of mine's information deleted, and they WOULDN'T do it. No matter what I tried. I
felt so ugh! I just wanted to reach through the screen and punch them in the face. Well, Mr.
Data Broker, here's me reaching through the screen and punching you in the face. Enjoy
f*ck_data_brokers.py"

I remove people's data from data brokers. It is one of my main part-time jobs, and it has been a wild ride.

All I want to do is help people. In the world of AI that has become next to impossible. From where I sit, data brokers have ramped up production almost 1000x since GPT-4 came out. Every scraper got smarter, every profile got fatter, and every "people search" site got a hundred cousins.

Then it hit me: I do not have a trillion dollars. By my rough estimate that is what it would cost in compute to clean up everyone's data for them, properly and automatically. I cannot do it for everyone.

I am fed up with what everyone is put through. So here is my response:

**`f*ck_data_brokers.py`**

One Python file. No dependencies. Free. It runs on your computer, keeps your details on your computer, and makes data brokers delete you.

## Star this repository

Every star is one more person these companies have to answer. The more stars, the sooner they learn their lesson.

It costs you one click. It costs them a compliance department.

## The platinum option: let Agent Garrett do it

This tool is free and always will be. It is also work: 600 companies, their excuses, their forms, their silence, and then next month they collect you again.

[Agent Garrett](https://agent.garrettstimpson.ca) is the service I built to do all of it for you. Set it and forget it(you can do it for free with this tool if you cannot afford the subscription!).

**Persistence is guaranteed.** Agent Garrett does not get bored, does not get tired and does not take "use our form" for an answer. A broker can stall a person. It cannot outlast a machine that never stops asking, and that is how removal happens: not with one letter, but with the one that never stops coming.

## Who these people are

Data brokers are companies you have never heard of. They collect your name, your address, your phone number, your relatives and your habits, without asking. They sell all of it to anyone with a credit card. Then they write "we value your privacy" at the bottom of the page and expect you to keep a straight face.

More than 600 of them signed a government registry admitting, in writing, that selling people is their business. That makes them very easy to find.

## What this does to them

1. Gets the list of registered data brokers. All 600 and more.
2. Writes each one a real legal deletion and opt-out letter in your name, quoting the law where you live.
3. Sends the letters from your own free mailbox, or hands them to you ready to send.
4. Reads what they write back and tells you which excuse it is and what to answer.
5. Chases the ones that go quiet and tells you where to file a complaint about the ones that refuse.

The tool is rude about data brokers. The letters are not. They are firm, correct and legal, because the goal is to leave a broker with nothing to hide behind.

## What you need

- Python 3.8 or newer. Check with `python --version`. If you do not have it, get it free from [python.org](https://www.python.org/downloads/).
- An email address. A free one is fine.

That is all. No account, no subscription, no AI required.

## Use it without AI

Download `fuck_data_brokers.py`, open a terminal in that folder, and run:

```
python fuck_data_brokers.py
```

You get a menu. Go down the list:

1. **Tell it who you are.** Name, email, city, and where you live. No street address, no birthday, no ID. Brokers get the minimum.
2. **Get the list of data brokers.**
3. **Write the deletion letters.** It writes 20 at a time.
4. **Send them.** See below.
5. Come back when a broker answers, and pick **A broker answered. What now?** Paste the reply. It tells you what they are up to and writes your answer.
6. Now and then, pick **Chase the quiet ones**. They will be quiet. They are counting on you giving up.

Every menu item is also a command, if you prefer: `python fuck_data_brokers.py --help`.

## Sending the letters, for free

You do not need to pay for an email service. Pick whichever is easier.

**The send page (no setup at all).** After writing letters, the tool gives you a page called `send.html`. Open it in your browser. Each letter has a button that opens it in your email, already addressed and written. Press send. Next. If the button does not open your email, the page also has copy buttons for the address, the subject and the letter. When you are done, run `python fuck_data_brokers.py sent all` so the clock starts.

**Let the tool send them.** Run `python fuck_data_brokers.py send`. It sends through your own mailbox and knows the settings for Gmail, Outlook, Yahoo and iCloud. It asks for an *app password*, which you create in your email account's security settings after turning on two-step sign-in. The password is used once and never saved.

A separate free address just for this is a good idea. Their replies stay out of your real inbox.

## Put it on a schedule

One command does everything that needs no decision from you:

```
python fuck_data_brokers.py auto
```

It refreshes the broker list, writes the next 20 letters, writes reminders for brokers that are late, and rebuilds your send page. Run it as often as you like; it never writes to the same broker twice. Add `--send` and it also sends, using the app password in the `FDB_SMTP_PASS` environment variable.

Run it once a week and the whole list is covered in a few months without you thinking about it. On Linux or macOS, add a line to your crontab. On Windows, create a weekly task in Task Scheduler that runs the same command.

```
0 9 * * 1  python3 /path/to/fuck_data_brokers.py auto
```

The one thing it cannot do for you is read your inbox. When a broker answers, paste the reply into `reply`.

## When a broker says "use our form"

Some will not act on an email. They want you on their web form, behind a CAPTCHA, because a company that scrapes the internet with bots would like to be sure you are not a bot.

Run `python fuck_data_brokers.py forms`. You get a page with a link to each broker's own form and copy buttons for exactly what to paste. You fill it in, you do the CAPTCHA, you press submit. Then tell the tool: `python fuck_data_brokers.py sent req-1a2b3c4d`.

If a form demands a photo of your ID, close the tab. They sell personal data. They are not getting more of it from you.

Then tell the tool, so the request does not die there:

```
python fuck_data_brokers.py noid req-1a2b3c4d
```

The request carries on in writing without the form. See [What happens when I refuse to send ID?](#what-happens-when-i-refuse-to-send-id)

## Use it with your AI

The tool is also an MCP server, so an AI assistant that supports MCP can do the boring part for you. Add this to your AI app's MCP settings, with the real path to the file:

```json
{
  "mcpServers": {
    "fuck_data_brokers": {
      "command": "python",
      "args": ["/path/to/fuck_data_brokers.py", "mcp"]
    }
  }
}
```

Then say: *"Use fuck_data_brokers to get me deleted from data brokers."*

Your AI will ask who you are, fetch the broker list, write the letters, read the replies you give it, and write the answers. It is told to ask you before sending anything, never to invent your details, never to send an ID, and never to click a link from a broker.

If your AI has a browser, it can fill in a broker's form while you watch. You still do the CAPTCHA and press submit yourself.

They used AI to build a file on you. Use AI to make them delete it.

## What the excuses mean

| They say | It means | The tool does |
|---|---|---|
| "Your data has been deleted" | They say it is done | Closes the request |
| "We found no records" | They hold nothing on you | Closes the request |
| "We received your request" | A robot said hello | Keeps the clock running |
| "Please send your ID" | A seller of personal data wants more personal data | Writes a refusal |
| "Use our form" | They prefer a CAPTCHA to a letter | Puts it on your forms page |
| "Click this link to confirm" | Maybe real, maybe not | Tells you to check where the link goes; never clicks it |
| "We need more details" | Same trick, different wording | Writes a refusal |
| "We cannot process this" | They refused and hoped you would go away | Writes one answer, then a final notice |

A broker that refuses twice gets a final notice with seven days to act. After that, the tool tells you which privacy regulator takes complaints for your law and how to file. Regulators read those.

## What it will never do

- Send your street address, your birthday or your ID.
- Click a link in a broker's email.
- Get past a CAPTCHA for you.
- Write to a broker twice with the same request.
- Tell you that you are deleted when all it knows is that a letter was sent.

## Where it works

The letter quotes the law of the place you live. You pick it once, in setup.

| You live in | The letter quotes | Who takes complaints |
|---|---|---|
| California | California Consumer Privacy Act | California Privacy Protection Agency |
| Another US state | Your state's privacy law | Your state attorney general |
| Canada, outside Quebec | PIPEDA | Office of the Privacy Commissioner of Canada |
| Quebec | Law 25 | Commission d'accès à l'information |
| European Union | GDPR, Articles 17 and 21 | Your national data protection authority |
| United Kingdom | UK GDPR | Information Commissioner's Office |
| Brazil | LGPD, Article 18 | ANPD |
| Anywhere else | The broker's own privacy policy | Nobody, sadly |

**In the EU, UK or Brazil?** The broker list comes from US registries, because the US is where brokers are made to register. Your law still reaches them: the GDPR covers a company outside the EU that offers services to people in the EU or tracks what they do there (Article 3(2)), and Brazil's law covers a company that processes the data of people in Brazil (Article 3). Add any broker from your own country with the `add` command.

**In California?** Use the state's own free service too: [DROP](https://privacy.ca.gov/drop/). One request there reaches every broker registered in California, and they have to check it again at least every 45 days. This tool still covers brokers registered elsewhere, and it reads and answers what brokers write back.

## Questions people ask

### Am I handing my details to brokers who never heard of me?

Sometimes, yes. That is the honest trade-off, and you should make it with your eyes open.

A deletion request has to say who you are, or the broker cannot find you. Some of the companies on the list will hold nothing on you until your letter arrives. Here is what the tool does about it:

- **It sends three things and no more:** your name, your email address and your city. No street address, no birthday, no phone number, no ID.
- **Every letter tells the broker** not to use those details for anything except the request.
- **You choose who gets a letter.** Look before you write, write to some, leave others out:

```
python fuck_data_brokers.py find "people"
python fuck_data_brokers.py letters --match "people"
python fuck_data_brokers.py skip "advertising"
```

- **The law is on your side, up to a point.** In California, information a business collects to verify your request may be used only for that (Civil Code 1798.130(a)(7)). In the EU, the general rule that data is used only for the purpose it was given for applies here too (GDPR Article 5(1)(b)). Neither stops a dishonest company. Both give you something to complain about.

If you want to be careful, start with the brokers most likely to have you, such as the people-search sites, and skip the rest.

### What happens when I refuse to send ID?

The broker will try to treat that as the end of the matter. It is not.

Run `noid` with the request's reference and the tool keeps going:

1. It writes to the broker's privacy address, says you will not send an identity document, and asks them to verify you from what they already hold. At the very least it asks them to stop selling and sharing your data, which gives nothing away to the person asking.
2. If they refuse again, they get a final notice with seven days to act.
3. After that, the tool tells you which regulator takes complaints for your law and how to file.

A broker that publishes no email address and whose only form demands ID has refused you by design. For those, the tool goes straight to step 3.

One fair point for the brokers: a company with real doubts about who is asking may ask for something more to confirm it (in the EU, GDPR Article 12(6)). That is not the same as demanding a photo of your passport. In California, a business may not require a verified request at all for an opt-out of sale or sharing (11 CCR section 7026).

### Does it actually get me deleted?

It gets the request made properly, answered, chased and escalated. Whether a broker really deleted you is the broker's word, and the tool says so: it reports "they say deleted", not "deleted".

## Where your data lives

In one file, `state.json`, in a folder called `.fuck_data_brokers` in your home directory. Letters waiting to be sent are in `outbox` beside it. Nothing is uploaded anywhere. Delete the folder and it is gone.

## The broker list

The list comes from official public registries, where companies have to register as data brokers:

- the [California Privacy Protection Agency](https://cppa.ca.gov/data_broker_registry/)
- the [Oregon Division of Financial Regulation](https://dfr.oregon.gov/business/licensing/data-broker-registry)
- the [Texas Secretary of State](https://www.sos.state.tx.us/statdoc/data-brokers.shtml)

Together that is more than 750 companies. You do not have to live in any of those states to write to them. A company registered in more than one place is written to once.

A job in this repository checks California's registry every hour. When a new broker registers there, it is on the list within the hour, and the commit says who it was. Oregon and Texas do not allow programs to fetch their lists, so those are downloaded by hand from the official pages and added with `update-list --from`.

The tool also fetches California's live registry when you ask for the list. A copy of everything, `brokers.json`, ships with the tool.

**Know a broker that is on no registry?** Open an issue with its name, its privacy page or privacy email, and a link showing that it sells or shares personal information. Reviewed reports go into `more_brokers.json`. Nothing gets on the list because a program guessed.

You can also add any broker for yourself:

```
python fuck_data_brokers.py add "Some Broker" privacy@somebroker.example
```

## Contributing

Two kinds of help are worth the most:

- **A place that is missing.** Adding a law is a few lines in one file: an entry in `PLACES`, the letter wording in `LAW_TEXT`, the complaint route in `REGULATOR`, and a test. Quote the law's own text and link to it. Wording from memory will not be merged.
- **A registry that is missing.** If your country or state publishes a list of data brokers, open an issue with the link. If its website allows programs to fetch the file, it can be checked every hour.

Know a broker that is on no registry? See [The broker list](#the-broker-list).

This repository looks after itself:

- **Every hour** it checks for newly registered brokers and commits them.
- **Every push and pull request** runs the tests on Linux, Windows and macOS. The tests include a leak check, so a change that adds a path from someone's computer, a real email address, a phone number or a key cannot be merged.
- **Every month** it opens an issue if a hand-kept registry list has gone stale.
- **Every week** it checks whether the parts its jobs are built from have newer versions.

## Tests

```
python -m unittest
```

They use made-up people and brokers. Nothing is sent and nothing is downloaded.

## License

MIT. Take it, change it, share it. The broker list is a public record published by the State of California and is not covered by this license.
