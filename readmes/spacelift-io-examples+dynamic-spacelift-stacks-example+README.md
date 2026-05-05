# Dynamic Spacelift Stacks Example
This repository shows an example implementation for dynamically creating Spacelift stacks based on folders dynamically detected.

## How does it work?
Most of the magic happens within the [locals.tf](locals.tf) file where we dynamically obtain and store the list of folders into variables, clean up this information, and filter out any paths we don't wish to create stacks for.

In this particular example, the `stack_paths_raw` local variable contains a list of all files under the root directory that contain a `main.tf` file, for Terragrunt users, you could replace this with `terragrunt.hcl`.

Next, the `stacks_clean_folders` local variable removes the `/main.tf` ending from each path and creates a new list that we can utilize for specifying the project_root of our stacks, as well as the name.

Finally, with the `stacks_clean_folders_filtered` local variable, we want to have the optional ability to filter out any paths we may not want to create paths for (e.g. the root `main.tf`). 

All of these locals get put to work in the [main.tf](main.tf) file, where we utilize a `for_each` loop based on the final outcome of `stacks_clean_folders_filtered`.

## Contribute
If you would like to contribute to this repository feel free to fork it and open a pull request and we'd be happy to take a look!
