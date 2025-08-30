#!/bin/bash
set -euo pipefail

echo "--- Claude Code Devcontainer Startup Script ---"

# Get current directory
CURRENT_DIR=$(pwd)

# Check if container exists and is running
CONTAINER_ID=$(docker ps -q --filter "label=devcontainer.local_folder=${CURRENT_DIR}" 2>/dev/null || true)

if [ -z "$CONTAINER_ID" ]; then
    echo "No running devcontainer found for ${CURRENT_DIR}"
    
    # Check if container exists but is stopped
    STOPPED_CONTAINER_ID=$(docker ps -a -q --filter "label=devcontainer.local_folder=${CURRENT_DIR}" 2>/dev/null || true)
    
    if [ -n "$STOPPED_CONTAINER_ID" ]; then
        echo "Found stopped container: $STOPPED_CONTAINER_ID"
        echo "Starting existing container..."
        docker start "$STOPPED_CONTAINER_ID"
        CONTAINER_ID="$STOPPED_CONTAINER_ID"
    else
        echo "No existing container found. Creating new devcontainer..."
        devcontainer up --workspace-folder .
        CONTAINER_ID=$(docker ps -q --filter "label=devcontainer.local_folder=${CURRENT_DIR}")
        
        if [ -z "$CONTAINER_ID" ]; then
            echo "ERROR: Failed to create or find devcontainer"
            exit 1
        fi
    fi
fi

echo "Using container: $CONTAINER_ID"
echo "Starting Claude with --dangerously-skip-permissions..."

# Start Claude in interactive session
docker exec -it "$CONTAINER_ID" zsh -c 'claude --dangerously-skip-permissions; exec zsh'