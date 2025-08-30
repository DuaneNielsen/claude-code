# Claude Code

![](https://img.shields.io/badge/Node.js-18%2B-brightgreen?style=flat-square) [![npm]](https://www.npmjs.com/package/@anthropic-ai/claude-code)

[npm]: https://img.shields.io/npm/v/@anthropic-ai/claude-code.svg?style=flat-square

Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows -- all through natural language commands. Use it in your terminal, IDE, or tag @claude on Github.

**Learn more in the [official documentation](https://docs.anthropic.com/en/docs/claude-code/overview)**.

<img src="./demo.gif" />

## Get started

1. Install Claude Code:

```sh
npm install -g @anthropic-ai/claude-code
```

2. Navigate to your project directory and run `claude`.

## Development Container Setup

This repository includes a devcontainer configuration for development with Claude Code:

### Quick Start with Devcontainer

Run the startup script to automatically handle container state and start Claude with unrestricted permissions:

```bash
./start_claude_dangerous.sh
```

This script will:
- Check for existing devcontainers and start/create as needed
- Launch Claude with `--dangerously-skip-permissions` flag
- Provide an interactive shell session

### Manual Devcontainer Usage

Alternatively, you can manually manage the devcontainer:

```bash
# Create and start the devcontainer
devcontainer up --workspace-folder .

# Connect to the running container
docker exec -it $(docker ps -q --filter "label=devcontainer.local_folder=$(pwd)") zsh
```

The devcontainer includes:
- Pre-installed Claude Code
- Python 3 with pip and venv
- uv (fast Python package manager)
- Development tools and utilities
- Disabled firewall for unrestricted internet access

### Rebuilding the Devcontainer

To rebuild the devcontainer after making changes to the configuration:

```bash
# Method 1: Using devcontainer CLI
devcontainer up --workspace-folder . --remove-existing-container

# Method 2: Manual Docker approach
# First, find and remove existing containers
docker ps -a --filter "label=devcontainer.local_folder=$(pwd)"
docker rm -f <container-id>

# Then rebuild
devcontainer up --workspace-folder .

# Method 3: If using VS Code
# Press Ctrl+Shift+P and select "Dev Containers: Rebuild Container"
```

### Data Persistence in Devcontainers

The devcontainer uses Docker volumes to persist important data between container restarts:

#### What Persists
- **Claude Code authentication and credentials** - stored in `/home/node/.claude/`
- **Shell command history** - stored in `/commandhistory/`
- **Project settings and configurations** - your Claude Code settings persist

#### How It Works
The devcontainer configuration creates persistent Docker volumes:
```json
"mounts": [
  "source=claude-code-bashhistory-${devcontainerId},target=/commandhistory,type=volume",
  "source=claude-code-config-${devcontainerId},target=/home/node/.claude,type=volume"
]
```

#### Volume Management
- **devcontainerId** is generated based on your project path and config
- Volumes survive container deletion and Docker Desktop restarts
- Each project gets isolated persistent storage

**Manual volume management:**
```bash
# List all Claude Code volumes
docker volume ls | grep claude-code

# Remove volumes (will lose all persistent data!)
docker volume rm claude-code-config-abc123def456

# Remove all unused volumes
docker volume prune
```

#### Security Note
Your Claude Code API keys and authentication tokens are stored in the persistent Docker volume at `/home/node/.claude/.credentials.json`. These credentials persist between container restarts but are isolated per project.

## Reporting Bugs

We welcome your feedback. Use the `/bug` command to report issues directly within Claude Code, or file a [GitHub issue](https://github.com/anthropics/claude-code/issues).

## Connect on Discord

Join the [Claude Developers Discord](https://anthropic.com/discord) to connect with other developers using Claude Code. Get help, share feedback, and discuss your projects with the community.

## Data collection, usage, and retention

When you use Claude Code, we collect feedback, which includes usage data (such as code acceptance or rejections), associated conversation data, and user feedback submitted via the `/bug` command.

### How we use your data

We may use feedback to improve our products and services, but we will not train generative models using your feedback from Claude Code. Given their potentially sensitive nature, we store user feedback transcripts for only 30 days.

If you choose to send us feedback about Claude Code, such as transcripts of your usage, Anthropic may use that feedback to debug related issues and improve Claude Code's functionality (e.g., to reduce the risk of similar bugs occurring in the future).

### Privacy safeguards

We have implemented several safeguards to protect your data, including limited retention periods for sensitive information, restricted access to user session data, and clear policies against using feedback for model training.

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).
