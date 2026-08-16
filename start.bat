@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
title SMAPCLASS - AI Attendance Platform
echo ========================================================
echo   Starting SMAPCLASS (All-in-One AI Attendance Platform)
echo ========================================================
if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe run.py
) else (
    python run.py
)
pause
