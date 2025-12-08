# ATLAS - Academic Task Learning Agent System
# Windows PowerShell Script for Easy Execution (with Virtual Environment)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ATLAS - Academic Task Learning Agent" -ForegroundColor Cyan
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

# Check if virtual environment exists
if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found!" -ForegroundColor Yellow
    Write-Host ""
    $create = Read-Host "Would you like to create one now? (y/n)"
    
    if ($create -ne "y" -and $create -ne "Y") {
        Write-Host ""
        Write-Host "Please run setup_venv.ps1 first to create a virtual environment:" -ForegroundColor Yellow
        Write-Host "  .\setup_venv.ps1" -ForegroundColor White
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host ""
    Write-Host "Running virtual environment setup..." -ForegroundColor Cyan
    & .\setup_venv.ps1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Virtual environment setup failed" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

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

# Check if .env file exists
if (-Not (Test-Path ".env")) {
    Write-Host "WARNING: .env file not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please create a .env file with your API key:" -ForegroundColor Yellow
    Write-Host "  NEMOTRON_4_340B_INSTRUCT_KEY=your_api_key_here" -ForegroundColor White
    Write-Host ""
    Write-Host "You can copy .env.example as a template:" -ForegroundColor Yellow
    Write-Host "  Copy-Item .env.example .env" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Environment file found!" -ForegroundColor Green
Write-Host ""

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
try {
    python -c "import langgraph" 2>&1 | Out-Null
    Write-Host "Dependencies already installed!" -ForegroundColor Green
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting ATLAS system..." -ForegroundColor Green
Write-Host ""

# Run the application
python main.py

# Pause to see any error messages
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Application exited with errors" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
