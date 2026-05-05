# ProjectM Music Visualization Service

This is a web service designed to run on AWS to convert audio files to video files by
running the audio data through the [projectM music visualizer](https://github.com/projectM-visualizer/projectm).

It makes use of the [projectM gstreamer plugin](https://github.com/projectM-visualizer/gst-projectm).

## Quickstart

Configure some AWS credentials and create a profile for the account you wish to deploy in.

If using an IAM user, run `aws configure`.

If using SSO, run `aws configure sso`.

Give your AWS profile a name.

```shell
npm i -g pnpm
pnpm install
pnpm exec cdk bootstrap --profile my-profile   # one-time setup
pnpm exec cdk deploy --profile my-profile
```
