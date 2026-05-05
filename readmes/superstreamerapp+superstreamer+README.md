<div align="center">
  <img src="./public/logo-mascotte.png" width="140" />

  <h3>Superstreamer</h3>
  <h4>From video processing to playback in a matter of minutes.</h4>
  
  <p align="center">
    <img src="https://img.shields.io/github/license/matvp91/superstreamer?v=1">
    <img src="https://img.shields.io/github/last-commit/matvp91/superstreamer?v=1">
    <img src="https://img.shields.io/github/stars/matvp91/superstreamer?v=1" alt="stars">
    <img src="https://img.shields.io/badge/PR's-welcome-0437F2" alt="pr">
    <a href="https://discord.gg/4hXgz9EsF4">
      <img src="https://img.shields.io/discord/1290252589522223166?v=1" alt="discord">
    </a>
  </p>

  <p align="center">
    <a href="https://superstreamer.xyz">Documentation</a> · 
    <a href="https://superstreamer.xyz/guide/getting-started.html">Getting Started</a> · 
    <a href="#contributing">Contributing</a>
  </p>

[<img src="./public/button-buy-me-a-coffee.png" width="150" alt="Buy me a coffee button"/>](https://www.buymeacoffee.com/matvp91)
[<img src="./public/button-join-discord.png" width="136" alt="Join Discord button"/>](https://discord.gg/4hXgz9EsF4)

</div>

Superstreamer is a self hostable platform that aims to simplify the complexities of video delivery. Transcode and package your media for online streaming with simple API calls and sane defaults, or craft dynamic HLS playlists on the fly with bumpers, ads and filters.

- Transcode your video file into separate quality tracks (eg; 1080p, 720p, 480p).
- Write `HLS CMAF` playlists directly to S3, ready for playback!
- Want to insert a bumper like Netflix? Stitch it as an HLS interstitial on the fly.
- Insert linear ads as interstitials by providing a simple VMAP, or schedule VAST manually.
- Use our player facade, a simplified API alongside [HLS.js](https://github.com/video-dev/hls.js), tailored for developers building a player UI.

Give us a ⭐ if you like our work. Much appreciated!

## Getting Started

```shell
# We have prebuilt containers, see docker/docker-compose.yml
cd docker
# Copy the example .env
cp .env.example .env
# Configure the .env
docker compose up -d
```

Self-hosting can be challenging, but we aim to make hosting Superstreamer as easy as possible. Check out the [Getting Started](https://superstreamer.xyz/guide/getting-started.html) section for more information. It should get you started in minutes.

## Screenshots

<div align="center">
  <a href="https://raw.githubusercontent.com/superstreamerapp/superstreamer/main/docs/public/dashboard-stitcher.png" target="_blank">
    <img width="400" alt="Dashboard stitcher" src="https://raw.githubusercontent.com/superstreamerapp/superstreamer/main/docs/public/dashboard-stitcher.png" />
  </a>
  <a href="https://raw.githubusercontent.com/superstreamerapp/superstreamer/main/docs/public/dashboard-api.png" target="_blank">
    <img width="400" alt="Dashboard stitcher" src="https://raw.githubusercontent.com/superstreamerapp/superstreamer/main/docs/public/dashboard-api.png" />
  </a>
  <a href="https://raw.githubusercontent.com/superstreamerapp/superstreamer/main/docs/public/dashboard-assets.png" target="_blank">
    <img width="400" alt="Dashboard assets" src="https://raw.githubusercontent.com/superstreamerapp/superstreamer/main/docs/public/dashboard-assets.png" />
  </a>
  <a href="https://raw.githubusercontent.com/superstreamerapp/superstreamer/main/docs/public/dashboard-job.png" target="_blank">
    <img width="400" alt="Dashboard job" src="https://raw.githubusercontent.com/superstreamerapp/superstreamer/main/docs/public/dashboard-job.png" />
  </a>
</div>

## Contributing

We love our contributors! Here's how you can contribute:

- [Open an issue](https://github.com/superstreamerapp/superstreamer/issues) if you believe you've encountered a bug.
- Follow the [local development guide](https://superstreamer.xyz/guide/getting-started.html) to set up your local dev environment.
- Make a [pull request](https://github.com/superstreamerapp/superstreamer/pull) to add new features or fix bugs.

<a href="https://github.com/superstreamerapp/superstreamer/graphs/contributors">
  <img width="200" src="https://contrib.rocks/image?repo=superstreamerapp/superstreamer" />
</a>

## Support

I've lost count of the weekends I’ve sacrificed to this project. If you think Superstreamer adding value to your company — or just want to help me remember what sunlight looks like — consider sponsoring! You can also pitch in by writing code, docs, or just spreading the word. Any help is hugely appreciated! 🥰
