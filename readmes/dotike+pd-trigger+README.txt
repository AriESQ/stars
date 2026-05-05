pd-trigger
==========

A lightweight, portable, and robust PagerDuty trigger utility.
--------------------------------------------------------------

The pd-trigger  utility can be used to trigger PD incidents, straight from the
shell, or any program.  pd-trigger is written in portable Bourne-ish sh(1),
implementing the the following Trigger API:

  https://developer.pagerduty.com/documentation/integration/events/trigger

### Dependencies

pd-trigger depends on the *curl(1)* utility, but is otherwise quite portable.

The authors are using it on the following platforms:

-   FreeBSD
-   Debian/Ubuntu Linux
-   OSX/Darwin

pd-trigger should work well on the following platforms as well,

-    OpenBSD
-    CentOS/RHEL
-    NetBSD
-    Illumos/Solaris
-    DragonFlyBSD

Can be run from cron(1), called from other UNIX programs, and receive stdout
in pipes from other programs, as plain text.


### Installation

pd-trigger is a very self-contained utility, and can be installed a number
of different ways.  A simple installer is included:

    $ ./install

If you run the installer as root, it will attempt to install into
/usr/local/bin by default.  If any other user, it will attempt to
install ~/bin for that user.  There are ENV overrides to allow 
changing install location, among other install details- read the
script for more info.


### Examples

prints help page,

    $ pd-trigger -h

When successfully exiting, default output behavior is to print the unique ID
of the event to stdout, as well as printing out into syslog(1) via logger(1).

Basic event trigger, no configuration:

  $ pd-trigger -r <API_routing_key>

To generate a config file (common use, to store an event routing_key):

  $ pd-trigger -c >> /etc/pd-trigger.conf
  # edit this file, add a PD event routing_key, and an
  #event can be triggered by simply running the program,
  $ pd-trigger

To trigger an alert message with a simple description,

  $ pd-trigger Hello, world.

  # or, same message via stdin,
  $ echo "Hello, world." | pd-trigger

  # or, the same message via explicit argument,
  $ pd-trigger -s "Hello, world."

To add a Link to the alert message,

  $ pd-trigger -u 'https://fqdn.tld/path' -s "Hello, world."

To ensure a new event is triggered (instead of appending to existing),

  $ pd-trigger -i Some new message.

You may use the '-' character to ensure cli parameter description string
is separated from option arguments, for example:

  $ pd-trigger -i -r 000000000 -v - Message which may have -c or other opt.

pd-trigger has more options which fully use the PagerDuty v2 API, which
makes this program flexible to use in your own scripts.


### Links

This utility is intended to conform to the PagerDuty v2 API trigger specification:

  https://developer.pagerduty.com/api-reference/b3A6Mjc0ODI2Nw-send-an-event-to-pager-duty

Instructions for generating an API Integration Key for a given service:

  https://support.pagerduty.com/docs/services-and-integrations#generate-a-new-integration-key

Alternatively, if you are looking for command line tools which do more than trigger events, be sure to check out the full-featured PagerDuty-CLI:

   https://github.com/martindstone/pagerduty-cli/wiki/PagerDuty-CLI-User-Guide

