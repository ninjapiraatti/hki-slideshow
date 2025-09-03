#!/bin/bash

# Path to your virtual environment folder
VENV_DIR="./venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Check if requirements.txt exists and install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing/updating dependencies from requirements.txt..."
    pip install -r requirements.txt > /dev/null 2>&1
fi

# Run the slideshow script with any arguments passed to this script
python slideshow.py "$@"

# Deactivate the virtual environment
deactivate