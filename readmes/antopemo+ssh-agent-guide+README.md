 Taken from:
 
  https://www.freecodecamp.org/news/the-ultimate-guide-to-ssh-setting-up-ssh-keys/ 
 
 All credits to them

# The Ultimate Guide to SSH - Setting Up SSH Keys

Welcome to our ultimate guide to setting up SSH (Secure Shell) keys. This tutorial will walk you through the basics of creating SSH keys, and also how to manage multiple keys and key pairs.

## Create a New SSH Key Pair
Open a terminal and run the following command:

```
ssh-keygen
```
You will see the following text:
```
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa):
Press enter to save your keys to the default /home/username/.ssh directory.
```
Then you'll be prompted to enter a password:
```
Enter passphrase (empty for no passphrase):

```
It's recommended to enter a password here for an extra layer of security. By setting a password, you could prevent unauthorized access to your servers and accounts if someone ever gets a hold of your private SSH key or your machine.
After entering and confirming your password, you'll see the following:
```
Your identification has been saved in /home/username/.ssh/id_rsa.
Your public key has been saved in /home/username/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:/qRoWhRcIBTw0D4KpTUyK6YepyL6RQ2CQrtWsaicCb4 username@871e129f767b
The key's randomart image is:
+---[RSA 2048]----+
| .o=+....        |
|+.*o+o .         |
|+X.=o o          |
|@.=.oo .         |
|=O ...o S        |
|o.oo . .         |
|.E+ . . . .      |
|oo . ... +       |
|=.. .o. . .      |
+----[SHA256]-----+
```
You now have a public and private SSH key pair you can use to access remote servers and to handle authentication for command line programs like Git.

## Manage Multiple SSH Keys
Though it's considered good practice to have only one public-private key pair per device, sometimes you need to use multiple keys or you have unorthodox key names. For example, you might be using one SSH key pair for working on your company's internal projects, but you might be using a different key for accessing a client's servers. On top of that, you might be using a different key pair for accessing your own private server.

Managing SSH keys can become cumbersome as soon as you need to use a second key. Traditionally, you would use `ssh-add` to store your keys to `ssh-agent`, typing in the password for each key. The problem is that you would need to do this every time you restart your computer, which can quickly become tedious.

A better solution is to automate adding keys, store passwords, and to specify which key to use when accessing certain servers.

### SSH config
Enter SSH config, which is a per-user configuration file for SSH communication. Create a new file: `~/.ssh/config` and open it for editing:
```
nano ~/.ssh/config
```
### Managing Custom Named SSH key
The first thing we are going to solve using this config file is to avoid having to add custom-named SSH keys using `ssh-add`. Assuming your private SSH key is named` ~/.ssh/id_rsa`, add following to the config file:
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa
  IdentitiesOnly yes
```

Next, make sure that `~/.ssh/id_rsa` is not in `ssh-agent` by opening another terminal and running the following command:
```
ssh-add -D
```
This command will remove all keys from currently active ssh-agent session.

Now if you try closing a GitHub repository, your config file will use the key at `~/.ssh/ida_rsa`.

Here are some other useful configuration examples:
```
Host bitbucket-corporate
        HostName bitbucket.org
        User git
        IdentityFile ~/.ssh/id_rsa_corp
        IdentitiesOnly yes
 ```       
Now you can use `git clone git@bitbucket-corporate:company/project.git`
```
Host bitbucket-personal
        HostName bitbucket.org
        User git
        IdentityFile ~/.ssh/id_rsa_personal
        IdentitiesOnly yes
```
Now you can use git clone `git@bitbucket-personal:username/other-pi-project.git`

```Host myserver
        HostName ssh.username.com
        Port 1111
        IdentityFile ~/.ssh/id_rsa_personal
        IdentitiesOnly yes
        User username
        IdentitiesOnly yes
   ```     
Now you can SSH into your server using `ssh myserver`. You no longer need to enter a port and username every time you SSH into your private server.

Password management
The last piece of the puzzle is managing passwords. It can get very tedious entering a password every time you initialize an SSH connection. To get around this, we can use the password management software that comes with macOS and various Linux distributions.

For this tutorial we will use macOS's Keychain Access program. Start by adding your key to the Keychain Access by passing `-K` option to the `ssh-add` command:

```
ssh-add -K ~/.ssh/id_rsa_whatever
```
Now you can see your SSH key in Keychain Access:

But if you remove the keys from `ssh-agent` with `ssh-add -D` or restart your computer, you will be prompted for password again when you try to use SSH. Turns out there's one more hoop to jump through. Open your SSH config file by running nano `~/.ssh/config` and add the following:

```
Host *
  AddKeysToAgent yes
  UseKeychain yes
 ``` 
With that, whenever you run ssh it will look for keys in Keychain Access. If it finds one, you will no longer be prompted for a password. Keys will also automatically be added to `ssh-agent` every time you restart your machine.

Now that you know the basics of creating new SSH keys and managing multiple keys, go out and ssh to your heart's content!