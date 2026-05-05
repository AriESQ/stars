# Ansible Playbook for installing the Ubiquiti Unifi Network Controller

An ansible playbook for installing the Unifi Network Controller.

![Unifi Network Controller Dashboard](img/unifi-dashboard.png)
## Supported Operating Systems

| OS | Notes
| :-- |  :-- |
| Debian 11 (bullseye) |  Recommended
| Ubuntu 22.04 LTS (jammy) |  Uses old libssl deb package for mongodb, uses focal for AdoptJDK repo
| Ubuntu 20.04 LTS (focal) | Uses old libssl deb package for mongodb

## Prerequisites

1. Ansible is installed in your PC ([instructions are here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible)).
2. One of the supported operating systems above is reachable by ssh.

## Usage

To run the playbook you will need the IP or hostname of the target server you want to install the Unifi controller on.

1. Open a terminal and run the following. The below command assumes you
````shell
TARGETPC=  # put your IP address, hostname or fqdn here. Can be comma separated for multiple servers

ansible-playbook unifi_network_controller_setup.yml -i $TARGETPC,
````
Append the following based on your how you connect to your server
````shell
--user myusername       # To connect with a specific user account
--ask-pass              # If an SSH password is required.
--become                # for sudo escalation
--ask-become-pass       # If you need to enter a password for sudo escalation.
````
example below:
````shell
TARGETPC=192.168.2.4

ansible-playbook unifi_network_controller_setup.yml -i $TARGETPC, --ask-pass --become --ask-become-pass --user larry
````
3. After installing you should be able to access the controller by using the following url:
````
https://{controller IP or fqdn}:8443
e.g. https://192.168.4.2:8443
````
4. Then accept the warning about the invalid certificate to go through the initial setup wizard.

## Notes
- MongoDB 3.x is the only release that is currently supported by the Unifi Network Controller. However 3.6 was retired in April 2021 and is now end of life. Unfortunately until Ubiquiti improves their mongodb support, 3.6 must be installed.
- If you would like to use a valid TLS certificate I would suggest to look into [acme.sh](https://github.com/acmesh-official/acme.sh/wiki/deployhooks#23-deploy-the-cert-on-a-unifi-controller-or-cloud-key) with LetsEncrypt as it has built in support for deploy hooks with the Unifi Network Controller. There is also an ansible community module for importing certificates into the Java Keystore over [here](https://docs.ansible.com/ansible/latest/collections/community/general/java_cert_module.html).
- A the time of writing, AdoptJDK did not have a repository release for 22.04 (jammy) and focal was used in its place.
- AdoptJDK is no longer supported and has moved over to [Eclipse Temurin](https://adoptium.net/en-GB/temurin/releases?version=8). I haven't tested moving to this variant yet and I was personally hoping for a repository to help keep it up to date. I will also consider [AWS Correto 8](https://docs.aws.amazon.com/corretto/latest/corretto-8-ug/downloads-list.html) as well, they also have their own debian packages. 

Are you interested to know more about the Unifi network controller? Want to know how layer 3 adoption works? Check out my postings for Unifi over at https://karubits.com/tags/unifi/ ❤️

