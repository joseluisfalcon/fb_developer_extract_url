#!/bin/bash

# Configuration
VENV_DIR=".venv"
TEST_SCRIPT="test_debugger.py"

echo "--- Running Facebook Developer URL Extractor Tests ---"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "[!] Error: Virtual environment not found. Please run ./install.sh first."
    exit 1
fi

# Activate virtual environment
# Support both Unix-like and Windows (Git Bash) paths
if [ -f "$VENV_DIR/Scripts/activate" ]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# Run tests
echo "[*] Executing pytest..."
pytest "$TEST_SCRIPT"

# Capture result
RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo ""
    echo "[✓] All tests passed successfully!"
else
    echo ""
    echo "[!] Some tests failed. Please check the output above."
fi

exit $RESULT
