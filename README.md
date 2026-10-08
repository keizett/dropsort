# 📦 DropSort

> **Turn messy folders into clean ones. — in one click.**

**DropSort** is a lightweight desktop file organizer that automatically sorts your files into neat categories based on their formats.

No cloud. No uploads. No complicated setup.
Just choose a folder → scan it → organize it. 🧹✨

---

## ✨ Features

* 📁 **One-click folder organization**
* 🖱️ **Drag & drop** support
* 🧠 **Automatic file categorization**
* 📸 **iPhone & Android media support**

  * HEIC / HEIF
  * JPG / JPEG
  * PNG / WEBP
  * MOV / MP4
  * 3GP / M4V
  * and more
* 📷 **RAW camera formats**

  * CR2 / CR3
  * NEF
  * ARW
  * DNG
  * RAF
  * RW2
  * and more
* 🎵 Audio
* 🎬 Video
* 📄 Documents
* 🗜️ Archives
* 💻 Source code
* 🎨 Design files
* 🔤 Fonts
* 💿 Installers
* 📝 Subtitles
* 🧲 Torrents
* 📦 Unknown formats → `Other`

### 🛡️ Duplicate-safe

DropSort never blindly overwrites an existing file.

If:

```text
photo.jpg
```

already exists, DropSort creates:

```text
photo (1).jpg
photo (2).jpg
```

instead.

Your files stay safe. 🔒

---

## 🎯 How it works

DropSort keeps things ridiculously simple:

```text
📂 Messy Folder
│
├── IMG_4821.HEIC
├── project.py
├── vacation.mp4
├── music.mp3
├── archive.zip
├── resume.pdf
└── random_file.xyz
```

↓

### DropSort

↓

```text
📂 Messy Folder
│
├── 📸 Images
│   └── IMG_4821.HEIC
│
├── 🎬 Videos
│   └── vacation.mp4
│
├── 🎵 Audio
│   └── music.mp3
│
├── 📄 Documents
│   └── resume.pdf
│
├── 🗜️ Archives
│   └── archive.zip
│
├── 💻 Code
│   └── project.py
│
└── 📦 Other
    └── random_file.xyz
```

One folder. Zero chaos. ✨

---

## 🖥️ Interface

DropSort comes with a clean dark desktop interface built with **PySide6**.

It shows:

* 📊 file statistics
* 📁 selected folder
* 📋 detected categories
* ⏳ organization progress
* ✅ final result

No terminal required.

---

## 🔐 Privacy

**DropSort is completely local.**

Your files:

* ❌ are not uploaded anywhere
* ❌ are not sent to an API
* ❌ are not analyzed by a cloud service
* ❌ do not leave your computer

Everything happens directly on your machine.

> Your files are yours. DropSort just helps clean them up. 🖤

---

## 🚀 Installation

Download the latest release from:

**GitHub → Releases**

Choose the version for your operating system.

### 🍎 macOS

Download:

```text
DropSort-macOS.zip
```

Extract it and launch:

```text
DropSort.app
```

### 🪟 Windows

Download:

```text
DropSort-Windows.zip
```

Extract the folder and launch:

```text
DropSort.exe
```

---

## 🧑‍💻 Run from source

Clone the repository:

```bash
git clone https://github.com/keizett/dropsort.git
cd dropsort
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

---

## 🛠️ Build

DropSort uses **PyInstaller** for standalone builds.

### macOS

```bash
chmod +x build_mac.sh
./build_mac.sh
```

### Windows

```text
build_windows.bat
```

Builds are also automatically generated through **GitHub Actions** when a release tag is pushed.

---

## 🧩 Tech Stack

| Technology        | Purpose           |
| ----------------- | ----------------- |
| 🐍 Python         | Core logic        |
| 🖥️ PySide6       | Desktop UI        |
| 📦 PyInstaller    | Standalone builds |
| ⚙️ GitHub Actions | Automated builds  |
| 🐙 GitHub         | Source & releases |

---

## 🗺️ Roadmap

DropSort started as a simple file organizer — but there's room to make it much smarter.

### v1.0

* [x] Automatic categorization
* [x] Drag & drop
* [x] Duplicate protection
* [x] iPhone / Android formats
* [x] RAW formats
* [x] macOS build
* [x] Windows build
* [x] GitHub Releases

### Future

* [ ] ↩️ Undo last organization
* [ ] 🔎 File search
* [ ] ⚙️ Custom categories
* [ ] 🚫 Ignore rules
* [ ] 📂 Recursive folder scanning
* [ ] 🖼️ Image previews
* [ ] 🧠 Smarter file detection
* [ ] 🍎 DMG installer
* [ ] 🪟 Windows installer
* [ ] 🌍 More languages

---

## ❤️ Why?

Because sometimes your Downloads folder looks like this:

```text
final_final2_REAL.zip
IMG_9382.HEIC
IMG_9383.HEIC
document(4).pdf
video.mp4
thing.zip
thing2.zip
test.py
random.png
????????.file
```

…and that's enough.

**DropSort exists to fix it.** 🧹

---

# 🇷🇺 Русская версия

## 📦 DropSort

> **Преврати хаос в папке в порядок. За один клик.**

**DropSort** — небольшое desktop-приложение, которое автоматически сортирует файлы по категориям в зависимости от их формата.

Без облака. Без загрузок. Без ебли с настройками.

Выбрал папку → запустил сортировку → получил порядок. 🧹✨

### ✨ Возможности

* 📁 автоматическая сортировка файлов
* 🖱️ Drag & Drop
* 📊 статистика найденных файлов
* 📸 поддержка фотографий iPhone и Android
* 🎬 поддержка видео
* 🎵 музыка и аудио
* 📄 документы
* 🗜️ архивы
* 💻 код
* 🎨 дизайн
* 🔤 шрифты
* 📷 RAW-фотографии
* 📝 субтитры
* 🧲 torrent-файлы
* 💿 установщики
* 📦 неизвестные форматы → `Other`

### 🛡️ Никаких случайных перезаписей

Если файл уже существует:

```text
photo.jpg
```

DropSort создаст:

```text
photo (1).jpg
```

вместо того чтобы уничтожить существующий файл.

### 🔐 Приватность

DropSort работает **полностью локально**.

Файлы:

* не загружаются в интернет;
* не отправляются на сервер;
* не передаются сторонним API;
* остаются на твоём компьютере.

> **Твои файлы — твои. DropSort просто наводит в них порядок. 🖤**

### 🚀 Скачать

Открой раздел **Releases** репозитория и скачай версию для своей системы.

### 🧑‍💻 Для разработчиков

```bash
git clone https://github.com/keizett/dropsort.git
cd dropsort

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python main.py
```

---

## 🖤 Made by keizett

Built with Python, PySide6 and a questionable amount of love for clean folders.

**DropSort — less chaos, more control.**
