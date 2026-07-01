@echo off
cd /d "%~dp0brain"

if not exist ".env" (
    echo Brak brain\.env - ustaw w nim GEMINI_API_KEY.
    pause
    exit /b 1
)

for /f "usebackq tokens=1,2 delims==" %%a in (".env") do set "%%a=%%b"

start "Mordo brain" cmd /k python main.py
timeout /t 2 >nul
start "" "pc_mordo.html"
