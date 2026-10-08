# DropSort

> Clean messy folders in one click.

DropSort is a small offline desktop utility that automatically sorts files into category folders by extension.

## Features

- Drag & drop a folder into the app
- Automatic file categorization
- iPhone / Android photo and video formats
- RAW camera formats
- Documents, archives, audio, code, fonts, design files and more
- Duplicate-safe renaming (`photo (1).jpg`)
- Progress bar and file statistics
- No cloud uploads
- macOS and Windows builds

## Supported categories

Images, Videos, Audio, Documents, Archives, Code, Fonts, Design, Subtitles, Torrents, Installers, Other.

## Run from source

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py main.py
```

## Build macOS app

```bash
python -m pip install pyinstaller
python -m PyInstaller --windowed --onedir --name DropSort main.py
ditto -c -k --sequesterRsrc --keepParent "dist/DropSort.app" "DropSort-macOS.zip"
```

## Build Windows app

Run on Windows:

```powershell
py -m pip install pyinstaller
py -m PyInstaller --windowed --onedir --name DropSort main.py
```

Zip `dist/DropSort/` and upload it to the GitHub Release.

## GitHub

Use a public repository such as `keizett/dropsort`. The included GitHub Actions workflow can build macOS and Windows archives when a `v*` tag is pushed.

## License

MIT
