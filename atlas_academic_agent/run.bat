@echo off
REM ATLAS - Academic Task Learning Agent System
REM Windows Batch Script for Easy Execution (with Virtual Environment)

echo ========================================
echo ATLAS - Academic Task Learning Agent
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

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo.
    echo Would you like to create one now?
    choice /C YN /M "Create virtual environment"
    if errorlevel 2 (
        echo.
        echo Please run setup_venv.bat first to create a virtual environment:
        echo   setup_venv.bat
        pause
        exit /b 1
    )
    if errorlevel 1 (
        echo.
        echo Running virtual environment setup...
        call setup_venv.bat
        if errorlevel 1 (
            echo ERROR: Virtual environment setup failed
            pause
            exit /b 1
        )
    )
)

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

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo.
    echo Please create a .env file with your API key:
    echo   NEMOTRON_4_340B_INSTRUCT_KEY=your_api_key_here
    echo.
    echo You can copy .env.example as a template:
    echo   copy .env.example .env
    echo.
    pause
    exit /b 1
)

echo Environment file found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import langgraph" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
) else (
    echo Dependencies already installed!
)

echo.
echo Starting ATLAS system...
echo.

REM Run the application
python main.py

REM Pause to see any error messages
if errorlevel 1 (
    echo.
    echo ERROR: Application exited with errors
    pause
)
