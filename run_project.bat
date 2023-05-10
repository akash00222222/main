@echo off
start /b python app.py
timeout /t 7 /nobreak >nul
start http://127.0.0.1:5000/
