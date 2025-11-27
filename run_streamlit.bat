@echo off
:: Check for Admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo *******************************************************
    echo This script must be run as Administrator!
    echo Right-click -> Run as Administrator
    echo *******************************************************
    pause
    exit /B
)

:: Navigate to project folder
cd /d %~dp0

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run Streamlit on safe port
set PORT=8508
set ADDR=127.0.0.1

echo Starting Streamlit app on http://%ADDR%:%PORT% ...
streamlit run run_app.py --server.port %PORT% --server.address %ADDR%

pause
