<div align="center">

[Website](https://browserable.ai) | [Documentation](https://docs.browserable.ai) | [Discord](https://discord.gg/b6s9fXNjeQ) | [Twitter](https://x.com/browserable)

![Browserable Logo](https://github.com/browserable/browserable/blob/main/docs/browserable-ai-invert.png?#gh-dark-mode-only)
![Browserable Logo](https://github.com/browserable/browserable/blob/main/docs/browserable-ai.png?#gh-light-mode-only)

## Open source browser automation library for AI agents
</div>

Browserable allows you to build browser agents that can navigate sites, fill out forms, clicking buttons and extract information. It is currently at 90.4% on the Web Voyager benchmarks.

## Quick start

The fastest way to get started is to run the npx command. This will guide you through the setup process and ensure you have all required dependencies.

```bash
npx browserable
```

Visit `http://localhost:2001` to set your LLM and Remote Browser API Keys to start using.

### Manual setup

Clone the repository:
  ```bash
  git clone https://github.com/browserable/browserable.git
  cd browserable
  ```

Pre-requisites:
  - Install [Docker](https://docs.docker.com/engine/install/)
  - Install [Docker Compose](https://docs.docker.com/compose/install/)

Start the development environment:
  ```bash
  cd deployment
  docker-compose -f docker-compose.dev.yml up
  ```

Set your API keys:
  - Open Browserable admin dashboard: [http://localhost:2001/dash/@admin/settings](http://localhost:2001/dash/@admin/settings).
  - Set API key of any one LLM provider (Gemini/ Open AI/ Claude).
  - Sign up for a free plan with any one remote browser provider ([Hyperbrowser](https://hyperbrowser.ai/)/ [Steel](https://steel.dev/)).
  - Set the API key of the remote browser provider in your [Browserable admin dashboard](http://localhost:2001/dash/@admin/settings).

## Services

Once running, you'll have access to the following services:

| Service | URL/Port | Description |
|---------|----------|-------------|
| UI Server | http://localhost:2001 | Main user interface |
| Documentation | http://localhost:2002 | Local documentation |
| Tasks Server | http://localhost:2003 | Task management API |
| MongoDB | 27017 | Database |
| MongoDB Express UI | http://localhost:3300 | Database management |
| Redis | 6379 | Caching and queues |
| MinIO API | http://localhost:9000 | Object storage API |
| MinIO Console | http://localhost:9001 | Object storage UI |
| DB Studio | http://localhost:8000 | Database management |

## JavaScript SDK

Install the SDK using npm:
```bash
npm install browserable-js
```

Or using yarn:
```bash
yarn add browserable-js
```

Here’s a simple example to get you started:

```typescript
import { Browserable } from 'browserable-js';

// Initialize the SDK
const browserable = new Browserable({
  apiKey: 'your-api-key'
});

// Create and run a task
async function runTask() {
  const createResult = await browserable.createTask({
    task: 'Find the top trending GitHub repos of the day.',
    agent: 'BROWSER_AGENT'
  });

  // Wait for task completion
  const result = await browserable.waitForRun(taskId);
  console.log('Results:', result.data);
}
```

## Demos

Task: On amazon.com search for a yoga mat at least 6mm thick, non-slip, eco-friendly, and under $50.

![amazon-demo](https://github.com/user-attachments/assets/98817aad-786d-43bc-8bbc-09ad33015fa5)

<br><br>
Task: On arxiv.org locate the latest paper within the 'Nonlinear Sciences - Chaotic Dynamics' category, summarize the abstract, and note the submission date.

![arxiv-demo](https://github.com/user-attachments/assets/c5e5a830-5050-4938-9832-2d2207c2720f)

<br><br>
Task: On coursera.com find a beginner-level online course about '3d printing' which lasts 1-3 months, and is provided by a renowned university.

![coursera-demo](https://github.com/user-attachments/assets/ea62d794-dccc-4517-a5be-6af82de9b5a5)






## Configuration options

Browserable offers configuration options for:
- LLM Providers
- Storage Solutions
- Database Systems
- Remote Browsers
- Custom Functions

For a complete list of environment variables and their configurations, see [Environment Variables Documentation](https://docs.browserable.ai/development/environment-variables).

## Documentation
See [browserable.ai/docs](https://docs.browserable.ai) for full documentation, or you can check the [REST API reference](https://docs.browserable.ai/rest-api/introduction)/ [JS SDK guide](https://docs.browserable.ai/js-sdk/introduction).

## Contributing

Browserable is an open-source and self-hostable project. We welcome contributions! 💛

Here's how you can help:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Added AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## Support

Questions/ feedback? [Join Discord](https://discord.gg/b6s9fXNjeQ).

## Acknowledgments

Some amazing open source projects Browserable wouldn't have been possible without: [bull](https://github.com/OptimalBits/bull), [mongo-express](https://github.com/mongo-express/mongo-express), [Stagehand](https://github.com/browserbase/stagehand), [Supabase](https://github.com/supabase/supabase).
