#!/bin/bash

# Configuration
VENV_DIR=".venv"
CONFIG_FILE="config_facebook_developer.json"
SAMPLE_FILE="config_facebook_developer.json.sample"

echo "--- Facebook Developer URL Extractor Setup ---"

# 0. Check Prerequisites
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "[!] Error: Python is not installed or not in PATH."
    exit 1
fi

if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "[!] Error: pip is not installed or not in PATH."
    exit 1
fi
if [ ! -d "$VENV_DIR" ]; then
    echo "[*] Creating virtual environment..."
    python -m venv "$VENV_DIR"
else
    echo "[✓] Virtual environment already exists."
fi

# 2. Activate Virtual Environment
# Support both Unix-like and Windows (Git Bash) paths
if [ -f "$VENV_DIR/Scripts/activate" ]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# 3. Install/Update Dependencies
echo "[*] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Check for Playwright
if ! python -c "import playwright" &> /dev/null; then
    echo "[!] Playwright not found after installation. Something went wrong."
else
    echo "[*] Ensuring Playwright browsers are installed..."
    playwright install chromium
fi

# 5. Check for Config File
if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo "[!] WARNING: $CONFIG_FILE not found."
    echo "    Please create it based on the sample file:"
    echo "    cp $SAMPLE_FILE $CONFIG_FILE"
    echo "    Then edit $CONFIG_FILE with your credentials/cookies."
else
    echo "[✓] Config file found."
fi

echo ""
echo "--- Installation Complete ---"
echo "You can now run the tool using: ./run.sh <URL>"
