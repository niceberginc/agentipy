@echo off
setlocal EnableDelayedExpansion

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM Activate virtual environment
if exist "%SCRIPT_DIR%.venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%.venv\Scripts\activate.bat"
) else (
    echo Virtual environment not found. Please run the installation steps in the README.
    exit /b 1
)

REM Load environment variables from .env file
if exist "%SCRIPT_DIR%.env" (
    for /f "usebackq tokens=1,* delims==" %%A in ("%SCRIPT_DIR%.env") do (
        set "%%A=%%B"
    )
) else (
    echo .env file not found. Please create one with your credentials.
    exit /b 1
)


REM Run the MCP server script
python "%SCRIPT_DIR%server.py"
