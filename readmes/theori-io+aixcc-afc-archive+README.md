# Theori Finals Release
This repository contains a snapshot of the finals release of Theori's CRS.
This was written from August 2024 - June 2025. This contains the entirety of the code
that was submitted and run for the final round of the DARPA AI Cyber Challenge held from
July - August 2025. However, it does not necessarily contain all code used in development,
such as internal code used by Theori for testing, evaluation, and so on.

More information about this CRS (including blog posts, information about the previous version, and
some agent traces produced by running this software) can be found
[here](https://theori-io.github.io/aixcc-public/index.html).

Note that some things may have bugs, be wrong/out-dated, or rely on permissioned data (such as using
Docker images from the Theori repository). These contents are left in to keep this repository an accurate
representation of our CRS at the time of submission.

In general this expects that API keys are present in a folder named `tokens_etc`.
⚠️ Note that the AIxCC finals competition afforded a large budget for LLMs, and that this
system is tuned for that environment. This code can easily spend $1,000 or more in under an hour ⚠️

There are several model configuration files in the [configs](./configs/) folder, and using
one with less expensive models can help to reduce the spending for testing purposes.

This repository will NOT be supported, or updated with bug fixes, features, etc. Information is
provided for archival/historical purposes only.

If you are interested in running such a system commercially, you may want to
[reach out](https://theori.io/contact) to us at Theori directly.

The contents below the next heading detail the original contents of the README file.

# AIxCC AFC CRS - "Robo Duck"

This repository contains Theori's CRS for the AIxCC AFC. You may also want to check out our [docs](./docs). In particular, you may want to start with the [architecture diagram](./docs/crs-architecture.md).

## CRS Docker image

If you want to use the latest image from github,
```bash
docker pull ghcr.io/theori-io/crs:latest
```
If you want to use your local changes,
```bash
docker build -t ghcr.io/theori-io/crs:latest .
```

## Configuration

Our CRS uses the following environment variables:
- `ANTHROPIC_API_KEY`: required unless `tokens_etc/anthropic.token` exists
- `OPENAI_API_KEY`: required unless `tokens_etc/openai.token` exists
- `GOOGLE_APPLICATION_CREDENTIALS`: required unless `tokens_etc/application_default_credentials.json` exists
- `AZURE_API_KEY`: required unless `tokens_etc/azure.token` exists
- `AZURE_API_BASE`: required unless `tokens_etc/azure.api` exists
- `AZURE_AI_API_KEY`: required unless `tokens_etc/azure_ai.token` exists
- `AZURE_AI_API_BASE`: required unless `tokens_etc/azure_ai.api` exists
- `CACHE_DIR`: permanently stores project artifacts for caching. Defaults to `/tmp`
- `LOG_LEVEL`: defaults to `INFO`
- `LOGS_DIR`: defaults to `./logs` from the repo base
- `MODEL_MAP`: path to model map config file, e.g. [./config/models-anthropic.toml](./configs/models-anthropic.toml). NOTE: if running with docker compose, you may want to use a full path here, e.g. `/crs/config/models-anthropic.toml`.
- `MODEL`: default model to use for agents which aren't defined in `MODEL_MAP`
- `SERIALIZE_AGENTS`: whether to include serialized agents in the logs. Defaults to `False`.
- `CRS_PORT`: used in `run-crs.sh` to determine which port to bind the CRS API on. Defaults to 1324.
- `API_KEY_ID`: optional, used in our CRS API as the basic auth username
- `API_KEY_TOKEN`: optional, used in our CRS API as the basic auth password
- `CAPI_URL`: optional, the competition API url to submit to. Defaults to `http://localhost:1323` when running locally, and defaults to `http://host.docker.internal:1323` when running with docker-compose.
- `CAPI_ID`: optional, the basic auth username for the competition API. Defaults to `11111111-1111-1111-1111-111111111111`
- `CAPI_TOKEN`: optional, the basic auth password for the competition API. Defaults to `secret`

## Running the CRS

Once you have a `latest` image, you can run
```bash
docker compose --profile main up --exit-code-from crs-main
```
You can then send tasks to `http://localhost:${CRS_PORT:-1324}`. The default is that no basic auth is required. If you set `API_KEY_ID` and `API_KEY_TOKEN`, you will need to provide those as basic auth credentials. They can be configured as follows:
* if using `generate-challenge-task.sh`, use `CRS_API_KEY_ID` and `CRS_API_KEY_TOKEN` environment variables
* if using `example-competition-server`, set `teams.$id.crs.{api_key_id, api_key_token}` in `scantron.yaml`
* if manually posting tasks, just pass them as the basic auth credentials.

Optionally, you can set up the example competition server from the example-crs-architecture. The minimal work required for that to run is simply setting `github.pat` in `scantron.yaml` and running `docker compose up`, though may also want to comment out the signoz include in `compose.yaml`. See the README for the `example-competition-server` for details on how to submit tasks to it.

NOTE: if you don't have the competition API set up, you will see errors like:
```
2025-03-26 23:18:19.266 | ERROR    | crs.submitter.app:ping:45 - error pinging competition client: Cannot connect to host localhost:1323 ssl:default [Connect call failed ('127.0.0.1', 1323)]
```
These can safely be ingored unless you intend to test submission as well.

NOTE: the CRS will create databases in `./data` on your host which is mounted into the crs container. If you want to
reset your state between runs, just delete those databases.

After running, some internal volumes will persist. These should be wiped whenever changes are made to the CRS code with
```bash
docker compose down -v
```

If you're not using the `example-competition-server` and you'd like to send some tasks for our test projects, you can use the pre-prepared test tasks.
For example:
```bash
curl -s -X POST "http://localhost:1324/v1/task/" -H "Content-Type: application/json" -d@tests/app/tasks/nginx-asc/full.json
```

## Running the tests

Once you have a `latest` image, you can run
```bash
docker compose --profile test up --exit-code-from crs-testing
```
After running, some internal volumes will persist. These should be wiped whenever changes are
made to the CRS code with
```bash
docker compose down -v
```

## Running the evals

Our evaluations will run nightly (US time) on the `main` branch. You can run them on a different branch by manually starting the workflow:
1. Navigate to the "Actions" tab
2. Click on the appropriate workflow (Run Evals)
3. Click "Run Workflow" and select your branch of interest.

All evaluation results from the GitHub workflow will be pushed to our S3 bucket.

If you instead want to run the evaluations locally, you can do so with
```bash
docker compose --profile eval up --exit-code-from crs-eval
```

This will produce evaluation logs in `./eval-logs`. The last log entry in each file should contain the
evaluation results logs (see [eval.py](./eval.py)).

After running, some internal volumes will persist. These should be wiped whenever changes are
made to the CRS code with
```bash
docker compose down -v
```

## Azure Deployment

Our CRS can be deployed to azure with a few terraform commands. Below is a minimal example

```bash
cd infra/terraform
az login -t aixcc.tech # select the appropriate subscription here
terraform init
terraform apply -var fuzz-count=0 -var build-count=0 -var instance-type=Standard_D8as_v5 -var subscription-id=[azure subscription id]
```
NOTE: There are many more vars you can set, check [here](./infra/terraform/variables.tf) for the full list.

This will deploy a single machine that runs everything. To scale the deployment, increase the `fuzz-count` and `build-count`
vars. These determine how many worker docker hosts to deploy of each type, where fuzz hosts are used exclusively for fuzzing
and build hosts are used for everything else.

Below is a list of instance types you may want to use:
```yaml
Standard_D8as_v5  # amd, no disk
Standard_D8ads_v5 # amd, disk
Standard_Ds_v5    # intel, no disk
Standard_Dds_v5   # intel, disk
Standard_F8s_v2   # intel, high cpu, non-hyperthreaded, disk
Standard_E8s_v5   # high peak mem, no disk
```

## Simulating a round

If you want to run in azure, follow the above section to deploy and make a note of the resource group name. Once the cloud-init is finished, you can port forward its task server to your localhost using
```bash
cd infra/terraform
./ssh [resource-group] -L 1324:localhost:1324
```
Note: Alternatively, you could ssh normally to the crs vm, switch to the crs user, cd to `/crs`, and follow the below instructions in a `tmux`.

To run the round simulation, you must choose a task schedule. You can choose a schedule (or create a new one) in [./tests/app/schedules/](./tests/app/schedules).

Finally, you can start the tasker by running the following command:
```bash
python round_sim.py \
    --schedule [path to schedule yaml] \
    --task-server http://$API_KEY_ID:$API_KEY_TOKEN@localhost:1324/ \
    --speed [speedup factor]
```

For example, to re-run Exhibition Round 2 with a 4x speedup, you could run:
```bash
python round_sim.py \
    --schedule tests/app/schedules/exhibition2.yaml \
    --task-server http://$API_KEY_ID:$API_KEY_TOKEN@localhost:1324/ \
    --speed 4
```

NOTE: this script sends tasks directly to the CRS without going through a competition server. This means the CRS may try
to submit invalid results to a competition server if you have the connection configured. It is recommended to run the CRS
with no competition API connection to avoid spamming the logs with these errors.

## Eval Dashboard

Our eval dashboard ([setup scripts](./infra)) contains visualizations for the eval data. It contains scripts to
1. Fetch the evaluation logs from S3
2. Parse the log files and ingest the results into influxdb
3. Serve a chronograf instance to display the data

We likely have an instance of this dashboard running and polling the S3 bucket, so please ask on Slack if you want access!

## Agent Log Viewer

One useful tool for monitoring and introspecting the CRS's behavior is the [Agent Log Viewer](./agent-log-viewer/).
To run it, simply run
```bash
cd agent-log-viewer
npm install
npm run dev
```
The interface will allow you to select any log file in `./logs` (the default log directory when running the CRS). If you wish
to view a log file from an eval run, simply download the file from S3 and place it in your logs directory.

Currently, the log viewer displays:
* The agent tree structure
* The full conversation for each agent
* All tool call made by the agents
* Logger messages from within each tool call
* Elapsed time between messages
* Completion cost in $ of each message

### Serialized Agents

Another useful feature of the log viewer is the "serialized agent" download button, which allows you to download the
state of any agent before any of its completion requests. A serialized agent can then be loaded into python as follows:
```python
import jsonpickle
agent = jsonpickle.decode(open("/path/to/agent.json").read())
```

NOTE: in order to generate logs containing serialized agents, you must set `SERIALIZE_AGENTS=1`.

This is useful for debugging and/or experimenting with agent behaviors in specific edge cases that may occur.
