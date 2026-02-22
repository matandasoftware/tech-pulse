@echo off
REM =============================================================================
REM Automated RSS Article Fetcher for Tech Pulse
REM 
REM This script:
REM - Activates Python virtual environment
REM - Runs Django management command to fetch articles
REM - Logs output with timestamp
REM - Designed for Windows Task Scheduler
REM
REM Author: Matanda Software
REM Created: 2026-02-22
REM =============================================================================

REM Set up paths
SET PROJECT_DIR=C:\Users\pfare\Projects\tech-pulse
SET VENV_DIR=%PROJECT_DIR%\venv
SET PYTHON=%VENV_DIR%\Scripts\python.exe
SET LOG_DIR=%PROJECT_DIR%\logs
SET LOG_FILE=%LOG_DIR%\fetch_articles.log

REM Create logs directory if it doesn't exist
IF NOT EXIST "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
    echo Created log directory: %LOG_DIR%
)

REM Navigate to project directory
cd /d "%PROJECT_DIR%"

REM Log start time
echo ====================================================================== >> "%LOG_FILE%"
echo SCHEDULED FETCH STARTED: %DATE% %TIME% >> "%LOG_FILE%"
echo ====================================================================== >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Run fetch command (output goes to log file)
"%PYTHON%" manage.py fetch_articles >> "%LOG_FILE%" 2>&1

REM Log end time
echo. >> "%LOG_FILE%"
echo ---------------------------------------------------------------------- >> "%LOG_FILE%"
echo FETCH COMPLETED: %DATE% %TIME% >> "%LOG_FILE%"
echo ====================================================================== >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Exit
exit /b 0