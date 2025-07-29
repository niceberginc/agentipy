#!/bin/bash

# Exit on error
set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environments
if [ -d "$SCRIPT_DIR/.venv" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
else
    echo "Virtual environment not found. Please run the installation steps in the README."
    exit 1
fi

# Load environment variables from .env file
if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
else
    echo ".env file not found. Please create one with your credentials."
    exit 1
fi

# Run the MCP server script
python "$SCRIPT_DIR/server.py"
