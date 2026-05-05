# AWS VPC Global Network Planner: planvpc

Article: https://matt.sh/aws-vpc


## What

`planvpc` generates a unified global IPv4 VPC network configuration for all AWS regions and
all availability zones for one or more accounts.

`planvpc` can optionally deploy your new global AWS VPC and Subnet configurations with Terraform automation.

You can use `planvpc` to generate terraform output which will use the included terraform `vpc-auto` module
to deploy your globally unique VPC configurations across all regions concurrently with one command.

Why should you care if your VPCs and AZs have non-overlapping subnets? Why not just live with
the defaults of letting AWS give you a single duplicated 172.31.0.0/16 by default in every
region? AWS has [VPC peering features](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html)
where you can bridge VPCs together even across accounts, but you can't combine VPCs if they
have duplicate (or overlapping) CIDR blocks.

When you plan your global network architecture up front in all regions (then throw away the default VPCs
if you aren't using them), you will be able to configure any region to directly talk to another
region internally without any IP conflicts or needing to rewind your internal architecture if you
want these features in the future.

## Basic Usage (generate a global network plan saved to JSON)

```bash
pip install poetry -U
git clone https://github.com/mattsta/aws-vpc-global-planner
cd aws-vpc-global-planner

poetry install

poetry run planvpc - build_subnets
```

## Sequential Usage

If your initial configuration is small enough, you can duplicate your subnet layout in
subsequent configurations for different accounts (so you can initiate VPC peering between
the same regions by guaranteeing globally unique subnets between two or more accounts).


```bash
poetry run planvpc --account_offset=1 - build_subnets
```

Sample CIDR blocks for first region generated (would start at 10.2.0.0/16 for `account_offset=0`):

```json
    "vpc": {
        "primary": "10.127.0.0/16",
        "secondary": [
            "10.128.0.0/16"
        ],
        "_unused": [
            "10.129.0.0/16",
            "10.130.0.0/16",
            "10.131.0.0/16"
        ]
    },
```


## Random Usage

Instead of using sequential VPC CIDR blocks starting at 10.2.0.0/16, 10.3.0.0/16, ..., you can ask
`build_subnets` to `--shuffle`, then all your VPC CIDR blocks will be assigned randomly
(Subnet selections will still be sequential inside each CIDR block though since those
CIDR block sub-allocations don't impact global interoperability between VPCs):

```bash
poetry run planvpc - build_subnets --shuffle
```

Sample output from generating a random CIDR block order instead of sequentially:

```json
        "vpc": {
            "primary": "10.169.0.0/16",
            "secondary": [],
            "_unused": [
                "10.17.0.0/16",
                "10.167.0.0/16",
                "10.37.0.0/16",
                "10.112.0.0/16"
            ]
        },
```


## Deploy Network Plan to Your Account, Globally

```
poetry run planvpc - build_subnets
poetry run planvpc - generate_terraform_config --profile=default
cat ./suggested.myregions.tf
terraform init
terraform plan
terraform apply
```

## Defaults

[By default](./planvpc/myregions.py) `planvpc` assumes:

- maximum regions to plan for: 20
- maximum CIDR blocks per VPC: 5
    - these are your `/16` supernets holding all your AZ subnets
    - Reserving 5 `/16` networks lets you allocate over 300k IPs per VPC
- az subnet allocation prefix: `/19` (8k IPs per subnet)
- subnet names per az: `["public", "internal"]`
- provisioning regions: see `PROVISION_ORDER` defaults
- account offset: 0 (increment if you need to provision multiple non-overlapping accounts)


## Customization

All parameters deciding the size, shape, or quantity of your generated network can be manually
specified by copying [`myregions.py`](./planvpc/myregions.py) to your running directory or you can
specify alternative arguments using command line options.

See: `poetry run planvpc --help`


## Design Decisions

We use [AZ IDs](https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html) instead of AZ names because
the IDs reflect the actual AZ location IDs and aren't randomly reassigned per account (`usw2-az4` is the same across
every account, while it could be any of `us-west-2[a-d]` between different accounts).

Maintaining actual AZ IDs is important because when you bridge VPCs because traffic is free only within the same physical AZ,
then costs more to talk across AZs, then costs even more to talk across regions.

## Output

### Console Example

```haskell
planvpc.regions:_establish_config:196 - Configuring with MAX_REGIONS=25 CONFIGURED_REGIONS=20 MAX_CIDR_BLOCKS_PER_VPC=5
planvpc.regions:_establish_config:203 - Configuring with AZ_SUBNET_PREFIX=19 ACCOUNT_OFFSET=0 SUBNET_TYPES=['public', 'internal']
planvpc.regions:_load_region_az_mapping:93 - [cache.myregions.json] Loading cached myregions...
planvpc.regions:build_subnets:232 - [regions max 25] [regions configured 17] HIGHEST VPC CIDR BLOCK PROVISIONED: 10.127.0.0/16
planvpc.regions:build_subnets:238 - You have 128 more /16s remaining (you can allocate 25.60 more VPCs since each allocates 5 /16s)
planvpc.regions:build_subnets:244 - You can repeat this config into 1.02 more accounts (128 unused VPC-level CIDR blocks)
planvpc.regions:build_subnets:273 - Current settings can allocate 40 /19 subnets (8,192 total IPs per subnet) per VPC (327,680 IPs in each VPC)
planvpc.regions:build_subnets:402 - [us-east-1] Using 1 secondary subnet!
planvpc.regions:build_subnets:339 - [us-west-1] Region has zone gaps: ['usw1-az1', 'usw1-az3'] (allocating for future use anyway)
planvpc.regions:build_subnets:339 - [ca-central-1] Region has zone gaps: ['cac1-az1', 'cac1-az2', 'cac1-az4'] (allocating for future use anyway)
planvpc.regions:build_subnets:299 - [eu-south-1] Skipping region because not available in account!
planvpc.regions:build_subnets:339 - [ap-northeast-1] Region has zone gaps: ['apne1-az1', 'apne1-az2', 'apne1-az4'] (allocating for future use anyway)
planvpc.regions:build_subnets:299 - [ap-southeast-3] Skipping region because not available in account!
planvpc.regions:build_subnets:299 - [ap-east-1] Skipping region because not available in account!
planvpc.regions:build_subnets:423 - [planned.myregions.json] Saved network plan
```

### Plan Example

Sample planning result (partial):

```json
{
    "us-east-1": {
        "subnets": {
            "public": {
                "use1-az1": "10.2.0.0/19",
                "use1-az2": "10.2.32.0/19",
                "use1-az3": "10.2.64.0/19",
                "use1-az4": "10.2.96.0/19",
                "use1-az5": "10.2.128.0/19",
                "use1-az6": "10.2.160.0/19"
            },
            "internal": {
                "use1-az1": "10.2.192.0/19",
                "use1-az2": "10.2.224.0/19",
                "use1-az3": "10.3.0.0/19",
                "use1-az4": "10.3.32.0/19",
                "use1-az5": "10.3.64.0/19",
                "use1-az6": "10.3.96.0/19"
            },
        },
        "vpc": {
            "primary": "10.2.0.0/16",
            "secondary": [
                "10.3.0.0/16"
            ],
            "_unused": [
                "10.4.0.0/16",
                "10.5.0.0/16",
                "10.6.0.0/16"
            ]
        }
    },
    "us-east-2": {
        "subnets": {
            "public": {
                "use2-az1": "10.7.0.0/19",
                "use2-az2": "10.7.32.0/19",
                "use2-az3": "10.7.64.0/19"
            },
            "internal": {
                "use2-az1": "10.7.96.0/19",
                "use2-az2": "10.7.128.0/19",
                "use2-az3": "10.7.160.0/19"
            }
        },
        "vpc": {
            "primary": "10.7.0.0/16",
            "secondary": [] ,
            "_unused": [
                "10.8.0.0/16",
                "10.9.0.0/16",
                "10.10.0.0/16",
                "10.11.0.0/16"
            ]
        }
    }
    ... 1,000 more lines ...
```

