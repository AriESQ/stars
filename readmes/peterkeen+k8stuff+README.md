# K8S Stuff

This is where I'm keeping my kubernetes stuff.

- `clusters` is where my clusters (at the moment just my homelab `omicron`) are defined
- `apps` is where all the workload definitions are. Some of these are just a single resource file, others are an entire buildable application.

I'm using Rake as a build/run tool.
The top level `Rakefile` loads every `.rake` file in the project, putting the tasks in a namespace defined by the directory structure.
For example, the file `clusters/omicron/tasks.rake` defines an `:apply` task, which would get loaded as `clusters:omicron:apply`.

