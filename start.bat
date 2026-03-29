@echo off
title NexGen Hospital
color 0B
echo.
echo  ================================================
echo   NexGen Hospital Management System
echo  ================================================
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo  Download from: https://python.org/downloads
    echo  Check "Add Python to PATH" during install
    pause & exit /b 1
)
echo  [OK] Python found

REM Create virtual environment if missing
if not exist "backend\venv" (
    echo  [SETUP] Creating virtual environment...
    python -m venv backend\venv
)

call backend\venv\Scripts\activate.bat

echo  [SETUP] Installing dependencies...
pip install -r backend\requirements.txt -q

echo.
echo  ================================================
echo  Make sure Neo4j Desktop is running first!
echo  Neo4j password must be: nexgen123
echo.
echo  Once started, open: http://localhost:8000
echo  Swagger API docs:   http://localhost:8000/docs
echo  ================================================
echo.

cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
