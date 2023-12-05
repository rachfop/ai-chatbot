#!/bin/bash

# Stop script on any error
set -e

# Optional: Clear the screen
clear

# Print the current version of Poetry
echo "Using Poetry version: $(poetry --version)"

echo "Installing dependencies..."
poetry install

# Completion message
echo "Completed successfully!"
