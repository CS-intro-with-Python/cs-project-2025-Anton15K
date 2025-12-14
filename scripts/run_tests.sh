#!/bin/bash
# Run tests locally with correct PYTHONPATH

# Ensure we are in the project root or adjust path
# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Export PYTHONPATH to include project root so 'Backend' module is found
export PYTHONPATH=$PROJECT_ROOT:$PYTHONPATH

# Run pytest
echo "Running tests from $PROJECT_ROOT..."
cd "$PROJECT_ROOT" && .venv/bin/pytest tests/ 
