@echo off
title DSA Algorithm Visualizer
color 0D

echo.
echo  =========================================
echo   DSA Algorithm Visualizer
echo   Sorting * Graphs * Linked List * Stack
echo  =========================================
echo.

cd /d "%~dp0"

echo  [1/3] Activating virtual environment...
call venv\Scripts\activate 2>nul
if errorlevel 1 (
    echo  Creating virtual environment first...
    python -m venv venv
    call venv\Scripts\activate
)

echo  [2/3] Checking packages...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo  Installing packages...
    pip install flask flask-cors requests -q
)

echo  [3/3] Starting backend on port 5001...
echo.
echo  =========================================
echo   Backend  : http://localhost:5001
echo   Frontend : open frontend\index.html
echo   Press CTRL+C to stop
echo  =========================================
echo.

start "" "frontend\index.html"

cd backend
python app.py

pause
