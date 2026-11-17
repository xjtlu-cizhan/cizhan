@echo off
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python not found. Please install Python 3 first: https://www.python.org/downloads/
  pause
  exit /b 1
)
title CiZhan Vocabulary Server
python server.py
pause
