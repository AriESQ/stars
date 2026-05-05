claude-podman
====

Claude for the security-conscious: run [claude-code, the claude cli tool](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), in a rootless [podman](https://podman.io/) container.

Installation
----

First, download and install podman. Installation is easy and secure with curl

```sh
curl --proto '=https' --tlsv1.2 -sSf \
  https://raw.githubusercontent.com/EvanCarroll/claude-podman/refs/heads/main/bin/claude |
  sudo tee /usr/local/bin/claude-podman
sudo chmod a+x /usr/local/bin/claude-podman
```

Now you can just run `claude-podman`.

Benefits
----

This provides the following benefits:

* Claude only gets file access to
	* Files in the present working directory
	* `$HOME/.claude.json`
	* `$HOME/.claude`
* Claude can only execute the files that exist in the image.

This image runs in rootless podman, and even inside rootless podman it runs as
a non-root user inside the container. Claude code is maximally locked down and
can't even update itself!

Customizing the runtime
----

Need to add packages to the container, or run an init script? no problem

```
--apk-packages foo,bar,baz # adds packages foo, bar, baz, with apk
--init-script  ./foobar.sh # copies foobar.sh into the container and executes it as root
```


For example, let's say you're using kubernetes and you do want claude to be able to troubleshoot it.

```sh
claude-podman \
	--apk-packages kubectl \
	--podman-arg "-v $HOME/.kube/config:/home/claude/.kube/config"
```
