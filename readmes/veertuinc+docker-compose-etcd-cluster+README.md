# `docker-compose` example for running an etcd cluster

1. Run `docker-compose up`
2. Run below test to ensure keys/values are distributed
		```
		watch -n 2 "set -x; curl -s http://127.0.0.1:2379/health; export RND=\$RANDOM; echo; docker exec -it etcd-1 /bin/sh -c \"etcdctl member list && etcdctl put \$RND bar && etcdctl get \$RND\" && docker exec -it etcd-2 /bin/sh -c \"etcdctl get \$RND\""
		```
		- If you see `bar` at the end, this means it was distributed across the cluster properly