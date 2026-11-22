@echo off
echo building...
pyinstaller --onefile --icon=icon.ico main.py
echo build complete!