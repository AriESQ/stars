# cloud-init kindergarten

A cloud-init playground in Docker (ubuntu 16.04).

Run it one-time with `docker-compose run dev`.

Edit `seed/user-data` file.

Re-run.

Profit.

Or do `docker-compose run dev bash`, and `rm -rf /var/lib/cloud/instance* && cloud-init init && cloud-init modules --mode=config && cloud-init -d modules --mode=final`. Any changes to the `seeds/user-data` will be picked-up.

