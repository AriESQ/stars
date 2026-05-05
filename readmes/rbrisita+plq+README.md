# Simple Python Service in a docker container and orchestrated by kubernetes.
## Setup
1. git clone git@github.com:rbrisita/plq.git
1. cd plq
1. docker-compose up -d

## Usage
Visit Docker's IP with Port to view index page to test Pig Latin Query.

# Testing Client
## Setup
1. virtualenv venv
1. source venv/bin/activate
1. pip install -r cli_requirements.txt

## Usage
python3 cli.py <ip:port> <pig_latin_query>
