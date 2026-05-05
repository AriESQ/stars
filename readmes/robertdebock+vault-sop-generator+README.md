# SOP Generator

Generate standard operating procedures (SOPs) for a specific Vault environment.

1. Fill in a customer value file. See `examples/*.yml` for examples.
2. Run `./generate.yml --extra-vars="@your-customer-values.yml"`

The output will be stored in `output/`.
