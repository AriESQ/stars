# AgentContainers

A pluggable agentic system framework for deploying AI assistants as containerized services via AWS Lambda or Docker containers. This project provides a generic abstracted interface for AI agents that can be accessed through various frontends (web UI, mobile apps, Slack, WhatsApp, etc.).

## Overview

AgentContainers allows you to run Claude Code and other AI agents in isolated, stateless containers that can be deployed as AWS Lambda functions or standalone Docker containers. The architecture consists of:

- **Shim Layer**: A Go-based request handler that translates HTTP/Lambda requests to Claude Code CLI commands
- **Agent Containers**: Docker images with pre-configured AI agents (currently includes a personal assistant implementation)
- **MCP Proxy**: Model Context Protocol proxy for extending agent capabilities with external tools
- **Persistent State**: Optional state management for session continuity across requests

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Anthropic API key (set in `.secrets` file as `ANTHROPIC_API_KEY=your-key`)

### Using Docker Compose

```bash
# Build the shim and assistant containers
docker-compose build shim
docker-compose build assistant

# Optional: Build MCP proxy if using external tools
docker-compose build mcp

# Run the assistant container with a simple request
docker-compose run --rm assistant '{"prompt":"who are you"}'
```

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Required - Your Anthropic API key for Claude access
- `LAMBDA`: Set to "true" for AWS Lambda execution mode (default: false)
- `MAX_TURNS`: Maximum conversation turns allowed per request (default: unlimited)
- `MODEL`: Claude model to use (e.g., "claude-3-5-sonnet-20241022", default: latest)
- `SYSTEM_PROMPT`: Override the default agent system prompt
- `FS_SHIM`: Enable filesystem state persistence (default: 1)
- `${NAME}_HOST`: URL for MCP proxy targets (e.g., `ASSISTANTSERVER_HOST=http://127.0.0.1:8080/mcp`)

### Request Format

The shim accepts JSON requests with the following structure:

```json
{
  "prompt": "Your request to the AI agent",
  "append_system_prompt": "Additional context to append to system prompt (optional)",
  "allowed_tools": ["Read", "Write", "Bash"], // Whitelist specific tools (optional)
  "disallowed_tools": ["WebFetch"], // Blacklist specific tools (optional)
  "resume_session_id": "session-123", // Resume previous session (optional)
  "env": {
    // Custom environment variables (optional)
    "CUSTOM_VAR": "value"
  }
}
```

### Response Format

The service returns an API Gateway-compatible response:

```json
{
  "statusCode": 200,
  "headers": null,
  "multiValueHeaders": null,
  "body": "{\"type\":\"result\",\"subtype\":\"success\",\"is_error\":false,\"duration_ms\":7634,\"duration_api_ms\":7089,\"num_turns\":1,\"result\":\"[Agent response here]\",\"session_id\":\"e2c3d429-413b-44be-9334-bff28c9953d0\",\"total_cost_usd\":0.114093,\"usage\":{...}}"
}
```

Key response fields in the body:

- `result`: The agent's text response
- `session_id`: ID for resuming this conversation later
- `is_error`: Whether the request failed
- `duration_ms`: Total execution time
- `total_cost_usd`: Estimated API usage cost
- `usage`: Token usage statistics

## Architecture

### Components

1. **Shim Layer** (`/shim/main.go`)

   - Translates JSON requests to Claude Code CLI arguments
   - Handles AWS Lambda or direct HTTP invocation
   - Manages environment variables and session state

2. **Assistant Container** (`/images/assistant/`)

   - Ubuntu 22.04 base image
   - Pre-installed Claude Code CLI
   - Configurable agent personas via system prompts
   - Development tools (git, zsh, fzf, etc.)
   - State persistence via mounted volumes

3. **MCP Proxy** (`/mcp/main.go`)
   - HTTP proxy for Model Context Protocol servers
   - Dynamic capability discovery
   - Tool, resource, and prompt registration
   - Enables integration with external services

### State Management

The system supports persistent state through filesystem mounting:

- Session history stored in `/mnt/state/projects/`
- SQLite database for metadata at `/mnt/state/__store.db`
- Symlinked to Claude's expected locations at runtime

## Development

### Prerequisites

- Go 1.23.3+
- Docker and Docker Compose
- AWS CLI (for Lambda deployment)

### Building from Source

```bash
# Build Go components
go build -o build/shim ./shim
go build -o build/mcp-proxy ./mcp

# Build Docker images
docker-compose build --no-cache
```

### Creating Custom Agents

1. Create a new Docker image based on the assistant template
2. Customize the `SYSTEM_PROMPT` environment variable
3. Add any agent-specific tools or configurations
4. Build and deploy your custom container

## AWS Lambda Deployment

### Building for Lambda

```bash
# Build the Lambda-compatible binary
GOOS=linux GOARCH=amd64 go build -o bootstrap ./shim

# Package for Lambda
zip function.zip bootstrap
```

### Lambda Configuration

- Runtime: `provided.al2` (Custom runtime)
- Handler: `bootstrap`
- Environment Variables:
  - `LAMBDA=true`
  - `ANTHROPIC_API_KEY=your-key`
  - Additional config as needed
- Timeout: Minimum 60 seconds recommended
- Memory: 512MB+ recommended

## Usage Examples

### Basic Query

```bash
docker-compose run --rm assistant '{"prompt":"What is the weather like today?"}'
```

### Resume Previous Session

```bash
docker-compose run --rm assistant '{
  "prompt": "Continue our previous conversation",
  "resume_session_id": "e2c3d429-413b-44be-9334-bff28c9953d0"
}'
```

### With Custom Tools

```bash
docker-compose run --rm assistant '{
  "prompt": "Help me analyze this codebase",
  "allowed_tools": ["Read", "Grep", "LS"],
  "disallowed_tools": ["Write", "Bash"]
}'
```

### Integration with External Services

```bash
# Set up MCP proxy for external service
export MYSERVICE_HOST="http://localhost:8080/mcp"

# Run with MCP integration
docker-compose run --rm assistant '{
  "prompt": "Use the external service to process this request",
  "env": {
    "MCP_SERVERS": "myservice"
  }
}'
```

## Current Implementation Status

### Implemented Features

- ✅ Personal Assistant Agent ("Clarice") - A comprehensive household management assistant
- ✅ Docker containerization with volume-based state persistence
- ✅ AWS Lambda compatibility
- ✅ Session resumption and conversation continuity
- ✅ Tool whitelisting/blacklisting
- ✅ MCP proxy for external tool integration
- ✅ Environment variable injection
- ✅ Cost tracking and usage reporting

### Roadmap

- [ ] Additional pre-built agent personas
- [ ] Web UI frontend
- [ ] Mobile app integration
- [ ] Slack/WhatsApp bot adapters
- [ ] Multi-agent orchestration
- [ ] Agent marketplace/registry
- [ ] Enhanced security features (sandboxing, resource limits)
- [ ] Distributed state management (Redis/DynamoDB)

## Contributing

Contributions are welcome! This project aims to provide a standardized way to deploy AI agents in production environments. Areas of interest:

- New agent implementations
- Frontend integrations
- Security enhancements
- Performance optimizations
- Documentation improvements

## License

This project is licensed under the GNU GPLv3 License with the [Commons Clause License Condition v1.0](https://commonsclause.com/).
