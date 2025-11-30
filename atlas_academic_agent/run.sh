#!/bin/bash
# ATLAS - Academic Task Learning Agent System
# Cross-platform run script (Linux/Mac)

echo "========================================"
echo "ATLAS - Academic Task Learning Agent"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/downloads/"
    exit 1
fi

echo "Python found!"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found!"
    echo ""
    read -p "Would you like to create one now? (y/n): " CREATE
    
    if [ "$CREATE" != "y" ] && [ "$CREATE" != "Y" ]; then
        echo ""
        echo "Please run setup.sh first to create a virtual environment:"
        echo "  ./setup.sh"
        exit 1
    fi
    
    echo ""
    echo "Running virtual environment setup..."
    bash ./setup.sh
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Virtual environment setup failed"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "Virtual environment activated!"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo ""
    echo "Please create a .env file with your API key:"
    echo "  NEMOTRON_4_340B_INSTRUCT_KEY=your_api_key_here"
    echo ""
    echo "You can copy .env.example as a template:"
    echo "  cp .env.example .env"
    echo ""
    exit 1
fi

echo "Environment file found!"
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
python -c "import langgraph" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
    
    echo "Dependencies installed successfully!"
else
    echo "Dependencies already installed!"
fi

echo ""
echo "Starting ATLAS system..."
echo ""

# Run the application
python main.py

# Check for errors
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Application exited with errors"
    exit 1
fi
