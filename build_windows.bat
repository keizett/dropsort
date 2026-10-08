@echo off
setlocal
py -m pip install -r requirements.txt
py -m pip install pyinstaller
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
py -m PyInstaller --windowed --onedir --name DropSort main.py
powershell -NoProfile -Command "Compress-Archive -Path 'dist\DropSort' -DestinationPath 'DropSort-Windows.zip' -Force"
echo Created: DropSort-Windows.zip
