# Microsoft Foundry Toolkit for Visual Studio Code

![Feature Highlight](https://aka.ms/ai-toolkit/feature-highlights-image)

## 🤖 What is Microsoft Foundry Toolkit

Microsoft Foundry Toolkit is the new name for AI Toolkit. It is a Visual Studio Code extension that helps you build AI agents quickly, with built-in access to [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry/) resources for model deployment, agent management, and more without leaving VS Code.

> 💡 **Note**: We have renamed this product to reflect its full integration with Microsoft Foundry. The previously separate Microsoft Foundry extension is now merged into this single extension. All existing features remain unchanged.

With Microsoft Foundry Toolkit you can:

- 🔍 **Discover and evaluate models** from providers including Microsoft Foundry, Foundry Local, Anthropic, OpenAI, GitHub, Google, and NVIDIA NIM, or run models locally with ONNX and Ollama.
- ⚡ **Build, test, and deploy AI agents** with Agent Builder for no-code prompt agents, or create code-based hosted agents with debugging, streaming visualization, and MCP tool integrations.
- ☁️ **Manage Microsoft Foundry resources** directly from VS Code: browse projects, deploy models from the catalog, and create, deploy, and test agents with the Microsoft Foundry Agent Service.

### ✨ Core Features

Features are grouped by workflow: models, agents, and the Microsoft Foundry resources that support both.

#### 🧠 Models

Everything you need to discover, test, customize, and optimize AI models.

| Feature | Description |
|---------|-------------|
| [Model Catalog](https://code.visualstudio.com/docs/intelligentapps/models) | Discover and access AI models from Microsoft Foundry, Foundry Local, GitHub, ONNX, Ollama, OpenAI, Anthropic, Google, and more. Compare models side-by-side and find the best fit for your use case. |
| [Playground](https://code.visualstudio.com/docs/intelligentapps/playground) | Interactive chat environment for real-time model testing. Experiment with different prompts, parameters, and multi-modal inputs including images and attachments. |
| [Fine-tuning](https://code.visualstudio.com/docs/intelligentapps/finetune) | Customize and adapt models for specific domains and requirements. Train models locally with GPU support or use Azure Container Apps for cloud-based fine-tuning. |
| [Model Conversion](https://code.visualstudio.com/docs/intelligentapps/modelconversion) | Convert, quantize, and optimize machine learning models for local deployment. Transform models from Hugging Face and other sources to run efficiently on Windows with CPU, GPU, or NPU acceleration. |
| [Profiling (Windows ML)](https://code.visualstudio.com/docs/intelligentapps/profiling) | Diagnose CPU, GPU, and NPU usage for running processes, ONNX models across execution providers, and Windows Machine Learning events. |

#### 🤖 Agents

Build, test, deploy, and observe AI agents end to end, from prompt agents to code-based hosted agents.

| Feature | Description |
|---------|-------------|
| [Create Agents](https://code.visualstudio.com/docs/intelligentapps/create-agents) | Create prompt agents with tools and vector stores, or build hosted agents with custom code. |
| [Agent Builder](https://code.visualstudio.com/docs/intelligentapps/agentbuilder) | Design prompt agents end to end: craft prompts, integrate MCP tools, define structured outputs, and generate production-ready code. |
| [Tool Catalog](https://code.visualstudio.com/docs/intelligentapps/tool-catalog) | Connect Microsoft Foundry tools and local MCP servers, then add those tools to agents in Agent Builder. |
| [Agent Inspector](https://aka.ms/AIToolkit/doc/test-tool) | Debug, visualize, and iterate on local and hosted agents directly in VS Code. |
| Deploy Hosted Agents | Deploy hosted agents from VS Code to the Microsoft Foundry Agent Service. Build and push container images to Azure Container Registry or upload a ZIP package, configure CPU and memory, set up RBAC, and manage versions for Microsoft Agent Framework and LangGraph projects written in Python, C#, or YAML. |
| Hosted Agent Playground | Test deployed hosted agents in an interactive playground with chat sessions, thread management, streaming responses, live container logs, OpenTelemetry traces, tool-call inspection, evaluation runs, and version switching. |
| [Evaluation](https://code.visualstudio.com/docs/intelligentapps/evaluation) | Assess models and agents using datasets and standard metrics. Measure performance with built-in evaluators (F1 score, relevance, similarity, coherence) or create custom evaluation criteria. |
| [Tracing](https://code.visualstudio.com/docs/intelligentapps/tracing) | Monitor and analyze AI application performance. Collect and visualize trace data to understand model and agent behavior and diagnose issues. |

#### ☁️ Microsoft Foundry resources

| Feature | Description |
|---------|-------------|
| Microsoft Foundry Resources | Browse Foundry projects, deploy language models from providers such as Microsoft, OpenAI, Meta, and DeepSeek, and create, deploy, and test agents with the Microsoft Foundry Agent Service. |

## 🚀 Getting started

New to Microsoft Foundry Toolkit? Start with a model, then turn your prompt into an agent. You do not need an Azure subscription for these first steps.

1. **Try GitHub-hosted models.** Open the [Model Catalog](https://code.visualstudio.com/docs/intelligentapps/models) and choose a model from the GitHub provider. Sign in with your GitHub account to chat with models in the [Playground](https://code.visualstudio.com/docs/intelligentapps/playground) without API keys or cloud setup.
2. **Create a local prompt agent in Agent Builder.** Open [Agent Builder](https://code.visualstudio.com/docs/intelligentapps/agentbuilder) to design a prompt agent end to end: craft your system prompt, attach MCP tools from the [Tool Catalog](https://code.visualstudio.com/docs/intelligentapps/tool-catalog), define structured outputs, and iterate on test runs inside VS Code.

When you're ready to move beyond local prototyping, connect your agent to [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry/) for managed hosting with the Foundry Agent Service, production-grade model deployments, evaluation at scale, tracing, and team collaboration from the same extension.

## 💬 Feedback and resources

We'd love to hear from you! Your feedback helps shape our roadmap.

- [Developer documentation](https://aka.ms/foundrytk/docs) — explore all features in depth
- [Tutorials](https://aka.ms/foundrytk/tutorial) — step-by-step guides to get started
- [GitHub Issues](https://aka.ms/AIToolkit/feedback) — report bugs or suggest new features
- [Discord community](https://aka.ms/azureaifoundry/discord) — connect with fellow developers

You can also send private bug reports or concerns to [vscai-support@microsoft.com](mailto:vscai-support@microsoft.com).

Microsoft Foundry Toolkit is built with and for the developer community.

## 📊 Data and telemetry

Microsoft Foundry Toolkit for Visual Studio Code collects usage data and sends it to Microsoft to help improve our products and services. Read our [privacy statement](https://go.microsoft.com/fwlink/?LinkId=521839) to learn more. This extension respects the `telemetry.enableTelemetry` setting—learn more at [disable telemetry reporting](https://code.visualstudio.com/docs/supporting/faq#_how-to-disable-telemetry-reporting).
