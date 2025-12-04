# ATLAS - Virtual Environment Setup Script (PowerShell)
# This script creates and configures a Python virtual environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ATLAS Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if virtual environment already exists
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
    Write-Host ""
    $recreate = Read-Host "Do you want to recreate it? (y/n)"
    
    if ($recreate -eq "y" -or $recreate -eq "Y") {
        Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force venv
        Write-Host "Old virtual environment removed." -ForegroundColor Green
        Write-Host ""
    }
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Virtual environment created successfully!" -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "You may need to set execution policy:" -ForegroundColor Yellow
    Write-Host "  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing project dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host ""
    Write-Host "You can try installing manually:" -ForegroundColor Yellow
    Write-Host "  1. Activate venv: .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  2. Install: pip install -r requirements.txt" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Cyan
try {
    python -c "import langgraph" 2>&1 | Out-Null
    Write-Host "All dependencies verified!" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Some dependencies may not have installed correctly" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your virtual environment is ready to use." -ForegroundColor White
Write-Host ""
Write-Host "To activate it manually:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run ATLAS:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Or simply run: .\run.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To deactivate when done:" -ForegroundColor Cyan
Write-Host "  deactivate" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
