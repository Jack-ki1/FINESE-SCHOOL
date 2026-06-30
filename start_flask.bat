@echo off
REM FINESE SCHOOL - Flask Startup Script for Windows
REM Run this file to start the application

echo ========================================
echo   FINESE SCHOOL - AI Tutor Platform
echo   Flask Version
echo ========================================
echo.

REM Check if Python is available
where py >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Checking setup...
py test_flask_setup.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Setup check failed. Please fix the issues above.
    pause
    exit /b 1
)

echo.
echo Starting Flask application...
echo.
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

py app.py

pause
