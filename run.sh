#!/bin/bash

VENV_DIR=".venv"
MAIN_SCRIPT="main.py"

# Help message
if [ "$#" -ne 1 ]; then
    echo "Usage: ./run.sh <URL>"
    echo "Example: ./run.sh https://www.example.com"
    exit 1
fi

URL="$1"

# Check if environment is set up
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found. Please run ./install.sh first."
    exit 1
fi

# Activate environment
if [ -f "$VENV_DIR/Scripts/activate" ]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# Run the script
echo "Starting extraction for: $URL"
python "$MAIN_SCRIPT" "$URL"
