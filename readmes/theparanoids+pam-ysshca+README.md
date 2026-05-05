# PAM-YSSHCA 
PAM-YSSHCA is the PAM module for YSSHCA (Yahoo SSHCA) certificate-based user authentication. 
The repo includes YSSHCA user certificates filters.

> A PAM module to authenticate a user by verifying a human or headless SSH user certificates from the ssh-agent.
> The module is designed for SUDO authentication.
>
> Future work: **Features for yubikey based touch-to-login and touch-to-sudo, and non-SSHAgent authentication (cryptoauth-client) is coming up next.**

## Table of Contents

- [Installation](#installation)
- [Example Usage](#example-usage)
- [Contribute](#contribute)
- [License](#license)

## Installation 

### Package Preparation 

---

**Option 1: Compile from Source**

#### 1. Package

Compile package for both deb and rpm by docker: 

```bash
$ docker run -v $PWD:/pam_sshca --rm golang /pam_sshca/package/package_linux.sh \
--package-name pam-sshca --package-version 0.0.1 --os-arch amd64 --package-type all
```

The packages are exported to `./_build` folder. 

```bash
$ ls ./_build/ 
pam-sshca-0.0.1-1.x86_64.rpm    pam-sshca_0.0.1_amd64.deb       pam_sshca.so
```

To specify the type of packaging: `all` (all types of packages), `deb` or `rpm`, by flag `--package-type`.
Please run `docker run -v $PWD:/pam_sshca --rm golang /pam_sshca/package/package_linux.sh --help` for more details.

> Tips:
> 
> (For Mac only) If you need Mac's ssh-agent forwarding into the docker container for Github access via SSH credentials, 
> please add docker's volume arguments `-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock`
> Note that you'll need to execute docker-for-mac from terminal (instead of GUI/spotlight) to let the docker engine recognize your SSH_AUTH_SOCK.    

#### 2. Install

* On Red Hat systems (RHEL, CentOS, etc):

```bash
rpm -ivh pam-sshca-0.0.1-1.x86_64.rpm
```

* On Debian-derived systems (Debian, Ubuntu, etc):

```bash
dpkg -i pam-sshca_0.0.1_amd64.deb 
```

#### 3. Configuration

* Add following pam_sshca authentication method into sudo pam config on your destination host: 

```bash
# /etc/pam.d/sudo
auth   [success=done default=die]   pam_sshca.so
```

You can customize the interface and the control flag of the share library in a proper order for the destination host. 

* Please review/edit your host's pam_sshca config at `/etc/pam_sshca.conf`. 
You may take a look at the [default config](./package/pam_sshca.conf). 

> Tips for `pam_sshca.conf`:
>
> * Filter: PAM_SSHCA provides filters as an extension mechanism to support arbitrary additional restrictions 
>           on — or rules for — acceptable credentials for authentication.
>           We provide an example filter [april-fools-filter](./example/april-fools-filter), 
>           which rejects user `April` by dropping certificates with principals containing the string "April" on April 1st.
>           You may compile the filter by `go build -o april-fools-filter`.
>           Then upload the binary to the host, save it with proper file permissions (owned by root with rwxr-xr-x), 
>           and set the filter path in the `pam_sshca.conf`. 
> 
>           Less frivolously, the owner of an extremely sensitive host which requires 2FA might choose to implement 
>           a customized filter that accepts _only_ certificates issued in the past 5 minutes. Such a filter would 
>           greatly reduce the time window during which an attacker could elevate privileges on that host via ssh agent hijacking. 

---

**Option 2: From Pre-built Packages**

> Note: Upcoming next

<!--- 
TODO: Publish PAM-SSHCA packages to github repo by Github Actions after the repo is open sourced. 
Ref:https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions
--->

---

## Example Usage

[comment]: <> (TODO: Add repo and section urls to following SSHRA/Crypki related links)

The example uses YSSHCA ([Crypki](https://github.com/theparanoids/crypki) as CA and [YSSHRA](https://github.com/theparanoids/ysshra) as RA) to provide YSSHCA ephemeral credentials,
which will be used to authenticate PAM_SSHCA module deployed in a docker container.

> **Disclaimer:**  Following example guidelines are to help you to get started with YSSHCA;
> they should be used only for testing/development purposes.
> In a production environment, a physical or cloud HSM should be used, and it's corresponding CA public key should be configured in PAM-SSHCA.

### Prerequisites

You will need following items to run the example:

* YSSHCA services ready: CA (Crypki) and RA (YSSHRA)
* The SSH user signing public key extracted from CA  

Following steps are provided to meet the requirements: 

[comment]: <> (TODO: Provide a more automatic way to setup YSSHCA \(docker compose file or k8s helm chart\) after both SSHRA and PAM-SSHCA are opensourced.)

#### 1. Setup Crypki and SSHRA

[comment]: <> (TODO: Add repo and section urls to following SSHRA/Crypki related links)
Please follow the SSHRA [User Guide]() to deploy Crypki and SSHRA locally.
Then you should have 2 services running on port 222 and 4443. 

```bash
$ docker ps
cffe8f5ffda6   sshra-local       "/etc/init.d/sshra s…"   4 hours ago   Up 4 hours   0.0.0.0:222->222/tcp     sshra
55ecff90b911   crypki-local      "/usr/bin/crypki-bin…"   5 hours ago   Up 5 hours   0.0.0.0:4443->4443/tcp   crypki
```

Refer to the section [CA credential]() in Crypki repo to extract the ssh user signing public key.
The public key the certificate authorities that are trusted to sign user certs for authentication.
The key identifier in Crypki in our example is `user_ssh_pub`.

```bash
docker cp crypki:/opt/crypki/slot_pubkeys/user_ssh_pub.pem ~/tmp/user_ssh_pub.pem 

# Convert the public key into Open SSH format, and save the key in `ysshca_uca` file.  
mkdir -p ./example/ssh-user
ssh-keygen -f ~/tmp/user_ssh_pub.pem -i -mPKCS8 > ./example/ssh-user/ysshca_uca
```

#### 2. Generate host ssh credentials for destination host (container).

```bash
pushd ./example
gen-ssh-crt.sh
popd
```

### Run the example

#### 1. Build a destination container with PAM SSHCA configured

`./example/docker-debian/Dockerfile` automates the process to build a debian image with OpenSSH and PAM_SSHCA installed. 

```bash
# point to the path of the deb package.
PAM_SSHCA_DEB_PATH=./_build/pam-sshca_0.0.1-1_amd64.deb 
docker build -f ./example/docker-debian/Dockerfile -t debian-pam-sudo --build-arg PAM_SSHCA_DEB_PATH=${PAM_SSHCA_DEB_PATH} .
```

#### 2. Run the destination host (container)

```bash
pushd ./exapmle
# $PWD/ssh-crt contains the host certs and $PWD/ssh-user contains the ca public key. 
docker run -d -p :223:22 -v $PWD/ssh-crt:/ssh-crt:ro \
-v $PWD/ssh-user:/ssh-user: \
--rm --name example_pam_debian debian-pam-sudo 
popd
```

Note: [Here](example/docker-debian/sshd_config) is a SSHD config example to enforce OpenSSH require YSSHCA certificates.

#### 3. Create an authorized user: `user_a`

Create user `user_a` with sudo permission inside the dest container.

```bash
USER='user_a'
docker exec example_pam_debian /etc/ssh/add_user.sh $USER
```

Refer to Section [YSSHCA Certificate Type]() in SSHRA repo to request a certificate with principal `user_a`.
The example takes a regular (touchless) certificate as an example:

```bash
$ssh-keygen -Lf <(ssh-add -L)
...
/dev/fd/63:14:
        Type: ssh-rsa-cert-v01@openssh.com user certificate
        Public key: RSA-CERT SHA256:psiQqqfGzADw4NR83WeJgTbnZ5oOlqbnC3ggncdGHHI
        Signing CA: RSA SHA256:mho4TPD8zXYmXT1Zx5EelKi4imBjwgyIBqYTm9X9YB0 (using rsa-sha2-256)
        Key ID: "{"prins":["user_a"],"transID":"15537d7b63","reqUser":"user_a","reqIP":"172.17.0.1","reqHost":"localhost","isFirefighter":false,"isHWKey":false,"isHeadless":false,"isNonce":false,"usage":0,"touchPolicy":1,"ver":1}"
        ... 
```

#### 4. Run SSH and SUDO 

We should be able to SSH against the sshra container now!

Note: To avoid `The authenticity of host '[localhost]:223 ([::1]:223)' can't be established` error,
you may either use SSH options `-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no` or
append the CA public key  `./example/ssh-crt/host_ca_key.pub` to your known host file `~/.ssh/known_hosts`.

```bash
$ echo "@cert-authority *" $(cat ./example/ssh-crt/host_ca_key.pub) >> ~/.ssh/known_hosts
 
$ ssh -A user_a@localhost -p 223
Authenticating YSSHCA Certificates  # YSSHCA banner defined in /etc/ssh/sshd_config    

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.

[user_a] $ whoami
user_a 

```

We will see a banner prompted by PAM_SSHCA when executing `SUDO`:

```bash

[user_a] $ sudo echo hello

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

[WARN] Failed to access syslogd, please fix your system logs.   # We didn't setup syslogd in the container. 
Authenticating by PAM_SSHCA...   # banner prompt defined in /etc/pam_sshca.conf
hello
```

## Contribute

Please refer to [Contributing.md](Contributing.md) for information about how to get involved.
We welcome issues, questions, and pull requests.

## License

This project is licensed under the terms of the [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) open source license. Please refer to [LICENSE](LICENSE) for the full terms.
