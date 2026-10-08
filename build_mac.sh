#!/bin/bash
set -euo pipefail
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller
rm -rf build dist DropSort-macOS.dmg
python3 -m PyInstaller --windowed --onedir --name DropSort --icon assets/dropsort.icns --osx-bundle-identifier com.keizett.dropsort main.py
mkdir -p dmg-root
rm -f dmg-root/Applications
cp -R "dist/DropSort.app" dmg-root/
ln -s /Applications dmg-root/Applications
hdiutil create -volname "DropSort" -srcfolder dmg-root -ov -format UDZO "DropSort-macOS.dmg"
rm -rf dmg-root

echo "Created: DropSort-macOS.dmg"
