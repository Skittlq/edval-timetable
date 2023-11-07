@echo off
python --version
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and run this installer again.
    pause
    exit /b 1
)