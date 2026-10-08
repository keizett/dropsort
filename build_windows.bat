@echo off
setlocal
py -m pip install -r requirements.txt
py -m pip install pyinstaller
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist installer-output rmdir /s /q installer-output
py -m PyInstaller --windowed --onedir --name DropSort --icon assets\dropsort.ico main.py
if not exist installer-output mkdir installer-output
where iscc >nul 2>&1
if errorlevel 1 (
    echo Inno Setup compiler not found. Install Inno Setup 6 first.
    exit /b 1
)
iscc installer.iss
echo Created: installer-output\DropSort-Setup.exe
