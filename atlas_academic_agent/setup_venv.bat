@echo off
REM ATLAS - Virtual Environment Setup Script (Windows Batch)
REM This script creates and configures a Python virtual environment

echo ========================================
echo ATLAS Virtual Environment Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if virtual environment already exists
if exist "venv\" (
    echo Virtual environment already exists.
    echo.
    choice /C YN /M "Do you want to recreate it"
    if errorlevel 2 goto :skip_recreate
    if errorlevel 1 goto :recreate
    
    :recreate
    echo Removing existing virtual environment...
    rmdir /s /q venv
    echo Old virtual environment removed.
    echo.
    
    :skip_recreate
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully!
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing project dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    echo You can try installing manually:
    echo   1. Activate venv: venv\Scripts\activate.bat
    echo   2. Install: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Verify installation
echo Verifying installation...
python -c "import langgraph" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed correctly
) else (
    echo All dependencies verified!
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your virtual environment is ready to use.
echo.
echo To activate it manually:
echo   venv\Scripts\activate.bat
echo.
echo To run ATLAS:
echo   python main.py
echo.
echo Or simply run: run.bat
echo.
echo To deactivate when done:
echo   deactivate
echo.
echo ========================================
echo.

pause
