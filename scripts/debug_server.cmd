@echo off

echo [Debug Server]

cd ../server

call ".venv/Scripts/python.exe" app.py

pause
