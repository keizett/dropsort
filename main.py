
from pathlib import Path
import random
import shutil
import sys

from PySide6.QtCore import Qt, QEvent, QTimer, QPointF, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QFileDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QMessageBox, QProgressBar,
    QPushButton, QScrollArea, QVBoxLayout, QWidget
)

CATEGORIES = {
    'Images': {
        '.jpg', '.jpeg', '.jpe', '.jfif', '.png', '.gif', '.webp',
        '.bmp', '.tif', '.tiff', '.heic', '.heif', '.avif', '.ico',
        '.svg', '.raw', '.cr2', '.cr3', '.nef', '.nrw', '.arw',
        '.dng', '.orf', '.rw2', '.raf', '.pef', '.srw', '.3fr',
        '.iiq', '.x3f'
    },
    'Videos': {
        '.mp4', '.m4v', '.mov', '.avi', '.mkv', '.webm', '.wmv',
        '.flv', '.mpeg', '.mpg', '.mpe', '.ts', '.mts', '.m2ts',
        '.3gp', '.3g2', '.ogv', '.vob', '.f4v', '.mxf'
    },
    'Audio': {
        '.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg', '.oga',
        '.opus', '.wma', '.aiff', '.aif', '.alac', '.amr',
        '.mid', '.midi', '.mka'
    },
    'Documents': {
        '.pdf', '.doc', '.docx', '.docm', '.odt', '.rtf', '.txt',
        '.md', '.tex', '.pages', '.epub', '.mobi', '.azw', '.azw3',
        '.xls', '.xlsx', '.xlsm', '.csv', '.ods', '.ppt', '.pptx',
        '.pptm', '.odp', '.numbers', '.key'
    },
    'Archives': {
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',
        '.tgz', '.tbz', '.zst', '.iso', '.dmg', '.cab'
    },
    'Code': {
        '.py', '.pyw', '.js', '.jsx', '.ts', '.tsx', '.html',
        '.htm', '.css', '.scss', '.sass', '.less', '.json',
        '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg',
        '.conf', '.c', '.h', '.cpp', '.hpp', '.cc', '.java',
        '.kt', '.kts', '.swift', '.m', '.mm', '.go', '.rs',
        '.rb', '.php', '.sql', '.sh', '.bash', '.zsh', '.fish',
        '.ps1', '.bat', '.cmd', '.lua', '.r', '.dart', '.vue',
        '.svelte', '.ipynb'
    },
    'Fonts': {'.ttf', '.otf', '.woff', '.woff2', '.eot'},
    'Design': {
        '.psd', '.ai', '.eps', '.indd', '.xd', '.fig', '.sketch',
        '.blend', '.fbx', '.obj', '.stl', '.3ds', '.max'
    },
    'Subtitles': {'.srt', '.ass', '.ssa', '.sub', '.vtt', '.sbv'},
    'Torrents': {'.torrent'},
    'Installers': {
        '.exe', '.msi', '.appx', '.msix', '.deb', '.rpm',
        '.pkg', '.apk'
    }
}

ORDER = list(CATEGORIES) + ['Other']
EXT = {ext: name for name, extensions in CATEGORIES.items()
       for ext in extensions}


def category(path):
    return EXT.get(path.suffix.lower(), 'Other')


def unique(path):
    if not path.exists():
        return path

    number = 1
    while True:
        candidate = path.with_name(
            f'{path.stem} ({number}){path.suffix}'
        )
        if not candidate.exists():
            return candidate
        number += 1


def files_in(folder):
    return [
        path for path in folder.iterdir()
        if path.is_file() and not path.name.startswith('.')
    ]


class DropArea(QFrame):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.setAcceptDrops(True)
        self.setObjectName('dropArea')

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for text, object_name in [
            ('📁', 'dropIcon'),
            ('Drop a folder here', 'dropTitle'),
            ('or choose a folder manually', 'muted')
        ]:
            label = QLabel(text)
            label.setObjectName(object_name)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                path = Path(url.toLocalFile())
                if path.is_dir():
                    self.callback(path)
                    break
        event.acceptProposedAction()


class Jmoji(QWidget):
    """Small animated mascot with cursor tracking and contextual speech."""

    speech_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFixedSize(112, 104)
        self.setMouseTracking(True)

        self.eye_x = 0.0
        self.eye_y = 0.0
        self.expression = 'normal'
        self.speech = 'hey.'
        self.click_count = 0
        self.setToolTip('Jmoji — click me')

        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.idle_line)
        self.idle_timer.start(6500)

        app = QApplication.instance()
        if app:
            app.installEventFilter(self)

    def say(self, text, expression=None):
        self.speech = text
        if expression:
            self.expression = expression
        self.speech_changed.emit(text)
        self.update()

    def idle_line(self):
        if not self.isVisible():
            return

        if random.random() < 0.55:
            self.say(random.choice([
                'still here.',
                'need a hand?',
                'your files await.',
                '...',
                'take your time.'
            ]), 'sleepy')

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseMove and self.isVisible():
            position = self.mapFromGlobal(event.globalPosition().toPoint())

            if self.rect().contains(position):
                cx, cy = self.width() / 2, 65
                dx = position.x() - cx
                dy = position.y() - cy
                length = max(1.0, (dx * dx + dy * dy) ** 0.5)

                self.eye_x = dx / length * 4
                self.eye_y = dy / length * 3
                self.update()

        return super().eventFilter(watched, event)

    def mousePressEvent(self, event):
        self.click_count += 1

        if self.click_count % 4 == 0:
            self.say('okay, okay.', 'surprised')
        else:
            self.say(random.choice([
                'what.',
                'yes?',
                'hello there.',
                'boop.',
                'you need something?'
            ]), 'happy')

        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Speech bubble
        bubble = self.rect().adjusted(2, 2, -2, -65)
        painter.setPen(QPen(QColor('#343740'), 1))
        painter.setBrush(QColor('#202229'))
        painter.drawRoundedRect(bubble, 9, 9)

        painter.setPen(QColor('#e8eaf0'))
        painter.setFont(QFont('Arial', 8))
        painter.drawText(
            bubble.adjusted(4, 0, -4, 0),
            Qt.AlignmentFlag.AlignCenter,
            self.speech
        )

        # Mascot body
        body = self.rect().adjusted(22, 38, -22, -5)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor('#f0f1f4'))
        painter.drawRoundedRect(body, 22, 22)

        # Eyes
        painter.setBrush(QColor('#18191d'))

        if self.expression == 'sleepy':
            painter.setPen(QPen(QColor('#18191d'), 2))
            painter.drawLine(
                QPointF(39 + self.eye_x, 65 + self.eye_y),
                QPointF(47 + self.eye_x, 65 + self.eye_y)
            )
            painter.drawLine(
                QPointF(64 + self.eye_x, 65 + self.eye_y),
                QPointF(72 + self.eye_x, 65 + self.eye_y)
            )
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            radius = 3.7 if self.expression != 'surprised' else 4.5

            painter.drawEllipse(
                QPointF(43 + self.eye_x, 65 + self.eye_y),
                radius, radius
            )
            painter.drawEllipse(
                QPointF(68 + self.eye_x, 65 + self.eye_y),
                radius, radius
            )

        # Tiny mouth
        painter.setPen(QPen(QColor('#18191d'), 1.5))
        if self.expression == 'happy':
            painter.drawArc(51, 68, 10, 6, 200 * 16, 140 * 16)
        elif self.expression == 'surprised':
            painter.drawEllipse(QPointF(56, 72), 2, 2)
        else:
            painter.drawLine(53, 73, 59, 73)


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder = None
        self.destination = None
        self.files = []

        self.setWindowTitle('DropSort')
        self.resize(850, 790)
        self.setMinimumSize(680, 650)

        root = QWidget()
        self.setCentralWidget(root)

        main = QVBoxLayout(root)
        main.setContentsMargins(28, 22, 28, 24)
        main.setSpacing(13)

        # Header
        header = QHBoxLayout()

        brand = QLabel('DropSort')
        brand.setObjectName('brand')

        subtitle = QLabel('Clean your folders in one click.')
        subtitle.setObjectName('muted')

        header.addWidget(brand)
        header.addSpacing(12)
        header.addWidget(subtitle)
        header.addStretch()

        self.jmoji = Jmoji()
        header.addWidget(self.jmoji)

        self.choose_button = QPushButton('Choose Folder')
        self.choose_button.clicked.connect(self.choose_source)
        header.addWidget(self.choose_button)

        main.addLayout(header)

        # Source folder
        main.addWidget(DropArea(self.set_source))

        self.source_label = QLabel('Source: no folder selected')
        self.source_label.setObjectName('path')
        self.source_label.setWordWrap(True)
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(self.source_label)

        # Batch mode switch
        self.batch_toggle = QCheckBox(
            'Batch Move — sort files into another folder'
        )
        self.batch_toggle.setObjectName('batchToggle')
        self.batch_toggle.toggled.connect(self.toggle_batch)
        main.addWidget(self.batch_toggle)

        self.batch_panel = QWidget()
        batch_layout = QVBoxLayout(self.batch_panel)
        batch_layout.setContentsMargins(0, 0, 0, 0)
        batch_layout.setSpacing(8)

        source_row = QHBoxLayout()
        source_row.addWidget(QLabel('Source folder'))
        source_row.addStretch()

        self.source_button = QPushButton('Choose source')
        self.source_button.clicked.connect(self.choose_source)
        source_row.addWidget(self.source_button)
        batch_layout.addLayout(source_row)

        destination_row = QHBoxLayout()
        destination_row.addWidget(QLabel('Destination folder'))
        destination_row.addStretch()

        self.destination_button = QPushButton('Choose destination')
        self.destination_button.clicked.connect(self.choose_destination)
        destination_row.addWidget(self.destination_button)
        batch_layout.addLayout(destination_row)

        self.destination_label = QLabel('No destination selected')
        self.destination_label.setObjectName('path')
        self.destination_label.setWordWrap(True)
        batch_layout.addWidget(self.destination_label)

        batch_note = QLabel(
            'Files are moved into category folders at the destination.'
        )
        batch_note.setObjectName('muted')
        batch_layout.addWidget(batch_note)

        main.addWidget(self.batch_panel)
        self.batch_panel.hide()

        # Actions
        actions = QHBoxLayout()
        actions.addWidget(QLabel('Organization:'))
        actions.addStretch()

        self.go = QPushButton('ORGANIZE FILES')
        self.go.setObjectName('primary')
        self.go.setEnabled(False)
        self.go.clicked.connect(self.organize)
        actions.addWidget(self.go)

        main.addLayout(actions)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        main.addWidget(self.progress)

        # File statistics
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.stats_widget = QWidget()
        self.stats = QGridLayout(self.stats_widget)
        self.stats.setContentsMargins(0, 0, 0, 0)
        self.stats.setSpacing(5)

        scroll.setWidget(self.stats_widget)
        main.addWidget(scroll, 1)

        footer = QLabel(
            'Offline • No uploads • Your files stay on your device'
        )
        footer.setObjectName('muted')
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(footer)

        self.refresh_button_state()

    def choose_source(self):
        start = str(self.folder) if self.folder else str(Path.home())
        selected = QFileDialog.getExistingDirectory(
            self, 'Choose source folder', start
        )

        if selected:
            self.set_source(Path(selected))

    def choose_destination(self):
        start = str(self.destination or Path.home())
        selected = QFileDialog.getExistingDirectory(
            self, 'Choose destination folder', start
        )

        if selected:
            self.destination = Path(selected)
            self.destination_label.setText(
                f'Destination: {self.destination}'
            )
            self.jmoji.say('destination acquired.', 'happy')
            self.refresh_button_state()

    def set_source(self, path):
        self.folder = path
        self.source_label.setText(f'Source: {path}')
        self.scan()

        self.jmoji.say('folder located.', 'happy')
        self.refresh_button_state()

    def toggle_batch(self, enabled):
        self.batch_panel.setVisible(enabled)

        if enabled:
            self.jmoji.say('two folders. got it.')
        else:
            self.jmoji.say('back to the usual.')

        self.refresh_button_state()

    def refresh_button_state(self):
        ready = self.folder is not None and bool(self.files)

        if self.batch_toggle.isChecked():
            ready = (
                ready
                and self.destination is not None
                and self.folder is not None
                and self.folder.resolve() != self.destination.resolve()
                and not self.destination.resolve().is_relative_to(
                    self.folder.resolve()
                )
            )

        self.go.setEnabled(ready)

    def scan(self):
        if self.folder is None:
            self.files = []
            self.render_stats()
            return

        try:
            self.files = files_in(self.folder)
        except OSError as error:
            self.files = []
            QMessageBox.warning(
                self, 'Cannot scan folder',
                f'Could not read this folder:\n{error}'
            )

        self.render_stats()
        self.refresh_button_state()

    def render_stats(self):
        while self.stats.count():
            item = self.stats.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        counts = {name: 0 for name in ORDER}

        for path in self.files:
            counts[category(path)] += 1

        row = 0

        for name in ORDER:
            if counts[name]:
                title = QLabel(name)
                value = QLabel(str(counts[name]))

                title.setObjectName('statName')
                value.setObjectName('statValue')
                value.setAlignment(Qt.AlignmentFlag.AlignRight)

                self.stats.addWidget(title, row, 0)
                self.stats.addWidget(value, row, 1)
                row += 1

        total = QLabel(f'{len(self.files)} files found')
        total.setObjectName('total')
        self.stats.addWidget(total, row, 0, 1, 2)

    def organize(self):
        if not self.folder or not self.files:
            return

        batch = self.batch_toggle.isChecked()

        source = self.folder.resolve()
        destination = (
            self.destination.resolve()
            if batch and self.destination
            else source
        )

        if batch:
            if source == destination:
                QMessageBox.warning(
                    self, 'Invalid folders',
                    'Choose different source and destination folders.'
                )
                return

            if destination.is_relative_to(source):
                QMessageBox.warning(
                    self, 'Unsafe destination',
                    'The destination cannot be inside the source folder.'
                )
                return

        mode_description = (
            f'from:\n{source}\n\nto:\n{destination}'
            if batch
            else f'inside:\n{source}'
        )

        answer = QMessageBox.question(
            self,
            'Confirm organization',
            f'Move {len(self.files)} files {mode_description}?\n\n'
            'Existing files will not be overwritten.',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.go.setEnabled(False)
        self.choose_button.setEnabled(False)
        self.source_button.setEnabled(False)
        self.destination_button.setEnabled(False)
        self.batch_toggle.setEnabled(False)

        total = len(self.files)
        moved = 0
        skipped = 0
        errors = []

        try:
            for index, path in enumerate(self.files, 1):
                try:
                    folder_name = category(path)
                    category_folder = destination / folder_name
                    category_folder.mkdir(parents=True, exist_ok=True)

                    target = unique(category_folder / path.name)

                    shutil.move(str(path), str(target))
                    moved += 1

                except (OSError, shutil.Error) as error:
                    skipped += 1
                    errors.append(f'{path.name}: {error}')

                self.progress.setValue(int(index / total * 100))
                QApplication.processEvents()

        finally:
            self.choose_button.setEnabled(True)
            self.source_button.setEnabled(True)
            self.destination_button.setEnabled(True)
            self.batch_toggle.setEnabled(True)

        self.scan()
        self.refresh_button_state()

        if skipped:
            self.jmoji.say('some files resisted.', 'surprised')
        else:
            self.jmoji.say('look at that. clean.', 'happy')

        message = f'Moved: {moved}\nSkipped: {skipped}'

        if errors:
            message += '\n\nFirst errors:\n' + '\n'.join(errors[:5])

        QMessageBox.information(self, 'DropSort', message)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('DropSort')
    app.setFont(QFont('Arial', 10))

    app.setStyleSheet("""
        QMainWindow, QWidget {
            background: #101114;
            color: #f2f2f2;
        }
        QLabel#brand {
            font-size: 28px;
            font-weight: 800;
        }
        QLabel#muted {
            color: #8f939c;
        }
        QLabel#path {
            color: #b9bdc7;
            padding: 8px;
        }
        QFrame#dropArea {
            border: 2px dashed #41454f;
            border-radius: 18px;
            min-height: 145px;
            background: #15171b;
        }
        QLabel#dropIcon {
            font-size: 42px;
        }
        QLabel#dropTitle {
            font-size: 20px;
            font-weight: 700;
            padding-top: 5px;
        }
        QPushButton {
            background: #24272e;
            border: 1px solid #3a3e47;
            border-radius: 10px;
            padding: 10px 14px;
        }
        QPushButton:hover {
            background: #2d3139;
        }
        QPushButton:disabled {
            color: #666b75;
        }
        QPushButton#primary {
            background: #f2f2f2;
            color: #101114;
            border: none;
            font-weight: 800;
            padding: 12px 20px;
        }
        QCheckBox#batchToggle {
            font-weight: 700;
            spacing: 10px;
            padding: 5px 0;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QComboBox {
            background: #181a1f;
            border: 1px solid #363a43;
            border-radius: 9px;
            padding: 9px 12px;
        }
        QProgressBar {
            background: #1a1c21;
            border: none;
            border-radius: 7px;
            height: 12px;
            text-align: center;
        }
        QProgressBar::chunk {
            background: #f2f2f2;
            border-radius: 7px;
        }
        QLabel#statName, QLabel#statValue {
            background: #17191e;
            padding: 11px;
            border-radius: 8px;
        }
        QLabel#statValue {
            font-weight: 700;
        }
        QLabel#total {
            padding-top: 12px;
            color: #9ca0aa;
        }
    """)

    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()