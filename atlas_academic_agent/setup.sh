#!/bin/bash
# ATLAS - Virtual Environment Setup Script (Linux/Mac)
# This script creates and configures a Python virtual environment

echo "========================================"
echo "ATLAS Virtual Environment Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python found: $PYTHON_VERSION"
echo ""

# Check Python version (need 3.9+)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo "ERROR: Python 3.9+ required, found $PYTHON_VERSION"
    exit 1
fi

# Check if virtual environment already exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
    echo ""
    read -p "Do you want to recreate it? (y/n): " RECREATE
    
    if [ "$RECREATE" = "y" ] || [ "$RECREATE" = "Y" ]; then
        echo "Removing existing virtual environment..."
        rm -rf venv
        echo "Old virtual environment removed."
        echo ""
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "Try installing python3-venv: sudo apt-get install python3-venv"
    exit 1
fi

echo "Virtual environment created successfully!"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "Virtual environment activated!"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing project dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo ""
    echo "You can try installing manually:"
    echo "  1. Activate venv: source venv/bin/activate"
    echo "  2. Install: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "Dependencies installed successfully!"
echo ""

# Verify installation
echo "Verifying installation..."
python -c "import langgraph" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Some dependencies may not have installed correctly"
else
    echo "All dependencies verified!"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Your virtual environment is ready to use."
echo ""
echo "To activate it manually:"
echo "  source venv/bin/activate"
echo ""
echo "To run ATLAS:"
echo "  python main.py"
echo ""
echo "Or simply run: ./run.sh"
echo ""
echo "To deactivate when done:"
echo "  deactivate"
echo ""
echo "========================================"
echo ""
