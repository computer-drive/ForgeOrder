@echo off

cd web
start npm run dev -- --host

cd ../server
start ".venv/Scripts/python.exe" app.py

cd ..