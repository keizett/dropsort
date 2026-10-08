#!/bin/bash
set -e
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller
rm -rf build dist
python3 -m PyInstaller --windowed --onedir --name DropSort main.py
ditto -c -k --sequesterRsrc --keepParent "dist/DropSort.app" "DropSort-macOS.zip"
echo "Created: DropSort-macOS.zip"
