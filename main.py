from pathlib import Path
import shutil
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication,QComboBox,QFileDialog,QFrame,QGridLayout,QHBoxLayout,QLabel,QMainWindow,QMessageBox,QProgressBar,QPushButton,QScrollArea,QVBoxLayout,QWidget
CATEGORIES={
'Images':{'.jpg','.jpeg','.jpe','.jfif','.png','.gif','.webp','.bmp','.tif','.tiff','.heic','.heif','.avif','.ico','.svg','.raw','.cr2','.cr3','.nef','.nrw','.arw','.dng','.orf','.rw2','.raf','.pef','.srw','.3fr','.iiq','.x3f'},
'Videos':{'.mp4','.m4v','.mov','.avi','.mkv','.webm','.wmv','.flv','.mpeg','.mpg','.mpe','.ts','.mts','.m2ts','.3gp','.3g2','.ogv','.vob','.f4v','.mxf'},
'Audio':{'.mp3','.wav','.flac','.aac','.m4a','.ogg','.oga','.opus','.wma','.aiff','.aif','.alac','.amr','.mid','.midi','.mka'},
'Documents':{'.pdf','.doc','.docx','.docm','.odt','.rtf','.txt','.md','.tex','.pages','.epub','.mobi','.azw','.azw3','.xls','.xlsx','.xlsm','.csv','.ods','.ppt','.pptx','.pptm','.odp','.numbers','.key'},
'Archives':{'.zip','.rar','.7z','.tar','.gz','.bz2','.xz','.tgz','.tbz','.zst','.iso','.dmg','.cab'},
'Code':{'.py','.pyw','.js','.jsx','.ts','.tsx','.html','.htm','.css','.scss','.sass','.less','.json','.xml','.yaml','.yml','.toml','.ini','.cfg','.conf','.c','.h','.cpp','.hpp','.cc','.java','.kt','.kts','.swift','.m','.mm','.go','.rs','.rb','.php','.sql','.sh','.bash','.zsh','.fish','.ps1','.bat','.cmd','.lua','.r','.dart','.vue','.svelte','.ipynb'},
'Fonts':{'.ttf','.otf','.woff','.woff2','.eot'},
'Design':{'.psd','.ai','.eps','.indd','.xd','.fig','.sketch','.blend','.fbx','.obj','.stl','.3ds','.max'},
'Subtitles':{'.srt','.ass','.ssa','.sub','.vtt','.sbv'},
'Torrents':{'.torrent'},
'Installers':{'.exe','.msi','.appx','.msix','.deb','.rpm','.pkg','.apk'}}
ORDER=list(CATEGORIES)+['Other']; EXT={e:c for c,es in CATEGORIES.items() for e in es}
def category(p): return EXT.get(p.suffix.lower(),'Other')
def unique(p):
    if not p.exists(): return p
    n,s=p.stem,p.suffix; i=1
    while True:
        q=p.with_name(f'{n} ({i}){s}')
        if not q.exists(): return q
        i+=1
class DropArea(QFrame):
    def __init__(self,cb):
        super().__init__(); self.cb=cb; self.setAcceptDrops(True); self.setObjectName('dropArea')
        l=QVBoxLayout(self); l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for t,obj in [('📁','dropIcon'),('Drop a folder here','dropTitle'),('or choose a folder manually','muted')]:
            x=QLabel(t); x.setObjectName(obj); x.setAlignment(Qt.AlignmentFlag.AlignCenter); l.addWidget(x)
    def dragEnterEvent(self,e):
        if e.mimeData().hasUrls(): e.acceptProposedAction()
    def dropEvent(self,e):
        for u in e.mimeData().urls():
            if u.isLocalFile() and Path(u.toLocalFile()).is_dir(): self.cb(Path(u.toLocalFile())); break
        e.acceptProposedAction()
class App(QMainWindow):
    def __init__(self):
        super().__init__(); self.folder=None; self.files=[]; self.setWindowTitle('DropSort'); self.resize(820,720); self.setMinimumSize(680,620)
        root=QWidget(); self.setCentralWidget(root); main=QVBoxLayout(root); main.setContentsMargins(28,24,28,24); main.setSpacing(16)
        h=QHBoxLayout(); b=QLabel('DropSort'); b.setObjectName('brand'); s=QLabel('Clean your folders in one click.'); s.setObjectName('muted'); h.addWidget(b); h.addSpacing(14); h.addWidget(s); h.addStretch(); o=QPushButton('Choose Folder'); o.clicked.connect(self.choose); h.addWidget(o); self.open=o; main.addLayout(h)
        main.addWidget(DropArea(self.set_folder)); self.path=QLabel('No folder selected'); self.path.setObjectName('path'); self.path.setAlignment(Qt.AlignmentFlag.AlignCenter); main.addWidget(self.path)
        c=QHBoxLayout(); c.addWidget(QLabel('Destination:')); self.mode=QComboBox(); self.mode.addItems(['Create category folders','Use existing category folders']); c.addWidget(self.mode); c.addStretch(); self.go=QPushButton('ORGANIZE FILES'); self.go.setObjectName('primary'); self.go.setEnabled(False); self.go.clicked.connect(self.organize); c.addWidget(self.go); main.addLayout(c)
        self.progress=QProgressBar(); self.progress.setValue(0); main.addWidget(self.progress)
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame); self.sw=QWidget(); self.stats=QGridLayout(self.sw); scroll.setWidget(self.sw); main.addWidget(scroll,1)
        f=QLabel('Offline • No uploads • Your files stay on your Mac/PC'); f.setObjectName('muted'); f.setAlignment(Qt.AlignmentFlag.AlignCenter); main.addWidget(f)
    def choose(self):
        p=QFileDialog.getExistingDirectory(self,'Choose a folder')
        if p: self.set_folder(Path(p))
    def set_folder(self,p): self.folder=p; self.path.setText(str(p)); self.scan(); self.go.setEnabled(bool(self.files))
    def scan(self):
        self.files=[p for p in self.folder.iterdir() if p.is_file() and not p.name.startswith('.')]; counts={c:0 for c in ORDER}
        for p in self.files: counts[category(p)]+=1
        while self.stats.count():
            w=self.stats.takeAt(0).widget()
            if w: w.deleteLater()
        r=0
        for c in ORDER:
            if counts[c]:
                a=QLabel(c); z=QLabel(str(counts[c])); a.setObjectName('statName'); z.setObjectName('statValue'); z.setAlignment(Qt.AlignmentFlag.AlignRight); self.stats.addWidget(a,r,0); self.stats.addWidget(z,r,1); r+=1
        t=QLabel(f'{len(self.files)} files found'); t.setObjectName('total'); self.stats.addWidget(t,r,0,1,2)
    def organize(self):
        if not self.folder or not self.files:return
        if QMessageBox.question(self,'Organize files',f'Move {len(self.files)} files into category folders?',QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)!=QMessageBox.StandardButton.Yes:return
        self.go.setEnabled(False); self.open.setEnabled(False); total=len(self.files); moved=skipped=0
        for i,p in enumerate(self.files,1):
            d=self.folder/category(p); d.mkdir(exist_ok=True); dest=unique(d/p.name)
            try: shutil.move(str(p),str(dest)); moved+=1
            except OSError: skipped+=1
            self.progress.setValue(int(i/total*100)); QApplication.processEvents()
        self.scan(); self.open.setEnabled(True); self.go.setEnabled(bool(self.files)); QMessageBox.information(self,'DropSort',f'Organized: {moved}\nSkipped: {skipped}')
def main():
    app=QApplication([]); app.setApplicationName('DropSort'); app.setFont(QFont('Arial',10)); app.setStyleSheet('''QMainWindow,QWidget{background:#101114;color:#f2f2f2} QLabel#brand{font-size:28px;font-weight:800} QLabel#muted{color:#8f939c} QLabel#path{color:#b9bdc7;padding:8px} QFrame#dropArea{border:2px dashed #41454f;border-radius:18px;min-height:220px;background:#15171b} QLabel#dropIcon{font-size:52px} QLabel#dropTitle{font-size:22px;font-weight:700;padding-top:8px} QPushButton{background:#24272e;border:1px solid #3a3e47;border-radius:10px;padding:11px 16px} QPushButton:hover{background:#2d3139} QPushButton:disabled{color:#666b75} QPushButton#primary{background:#f2f2f2;color:#101114;border:none;font-weight:800;padding:12px 20px} QComboBox{background:#181a1f;border:1px solid #363a43;border-radius:9px;padding:9px 12px;min-width:210px} QProgressBar{background:#1a1c21;border:none;border-radius:7px;height:14px;text-align:center} QProgressBar::chunk{background:#f2f2f2;border-radius:7px} QLabel#statName,QLabel#statValue{background:#17191e;padding:11px;border-radius:8px} QLabel#statValue{font-weight:700} QLabel#total{padding-top:12px;color:#9ca0aa}'''); w=App(); w.show(); app.exec()
if __name__=='__main__': main()
