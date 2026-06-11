# agentyesno

# Why?

Didn't you always want to use SSH agent forwarding when connecting to vaguely
trusted computers? Me neither. Sometimes one may have to and in that case
`agentyesno` might be useful.

`agentyesno` is a tiny interactive terminal program which acts an intercepting
proxy for SSH agent protocol's Sign Requests. It is meant to stand between
remote agent requests and your local SSH agent. It *may* work with local agent
requests, but local clients can easily circumvent the agent.

# Disclaimer

Use `agentyesno` at your own risk. It is untested and experimental. This kind of
a tool may offer you some protection in certain scenarios, but there are many
scenarios where it will not help you. There is a reason why for example OpenSSH
does *not* enable forwarding of agent connections by default. If you don't know
what you are doing, do not use agent forwarding. Before you use a tool like
this, make sure that ProxyJump (`-J`), locking the agent (`-x`) or ProxyCommand
are not better suited for your needs.

# How does it work?

`agentyesno` uses Go's SSH library for handling client and agent communications.
The program pauses on Sign Requests and asks the user's opinion before passing
the request to the actual agent. The user has to explicitly accept this sign
request by typing something. If the user does not give permission or responding
takes too long, then the Sign Request is dropped and not forwarded to the actual
agent. All other supported agent operations are passed transparently and
non-interactively.

```

     Sign                       Sign
    Request                    Response

           .---------------.
      /|\  |   ssh agent   |      |
       |   '---------------'      |
       |         |                |
       |         | domain socket  |
       |         |                |
       |   .---------------.      |
       |   |   agentyesno  |      |
       |   '---------------'      |
       |         |                |
       |         | domain socket  |
       |         |                |
       |   .---------------.      |
       |   |  agent client |     \|/
           '---------------'
```


To make usage clearer, `agentyesno` will only serve one Sign Request at a time.
Other clients will have to wait for their turn.

# How to use?

## Summary

1. Run `agentyesno` and make sure it can find the real SSH agent either with
   `$SSH_AUTH_SOCKET` or with the `-agent` parameter
2. Connect to some SSH server using `ssh` with agent forwarding enabled and make
   sure `$SSH_AUTH_SOCK` points at `agentyesno`

## Details

`agentyesno` listens on a domain socket as locally running SSH agents typically
do and you instruct your SSH client to use `agentyesno` as the agent. With
OpenSSH, this would mean setting your `$SSH_AUTH_SOCK` to point at `agentyesno`'s
listening socket on the filesystem, perhaps like this:

    $ export SSH_AUTH_SOCK="$(agentyesno -printlisten)"

If you don't wish to make the change persist in the shell session, you can set
the value for a single program execution:

    $ SSH_AUTH_SOCK="$(agentyesno -printlisten)" ssh user@host

Somewhere on the background and easily reachable, perhaps in a different
terminal window or a tmux pane, you would have `agentyesno` ready and waiting
for agent requests:

    $ agentyesno

`agentyesno` will default to finding your real agent via `$SSH_AUTH_SOCK`. You
may also set the listening socket and real agent paths with `-listen` and
`-agent`, respectively.

For more instructions, see the program code and the help:

    $ agentyesno -h

# How to install?

If you have a Go toolchain installed, you can install the latest tagged version of
`agentyesno` by invoking

    $ go install github.com/susji/agentyesno@latest

Alternatively, [here](https://github.com/susji/agentyesno/releases) you will
find pre-built binaries for several architectures and UNIX-like platforms.
