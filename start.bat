@echo off
echo Starting FastAPI server...
uvicorn app:app --reload

REM Wait for the server to start before opening the browser
timeout /t 3 /nobreak > nul

REM Open the browser after the server starts
start "" "http://127.0.0.1:8000"