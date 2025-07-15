# collage_widget.py (gestylede versie)
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QTextEdit,
    QSpinBox, QProgressBar, QFileDialog, QScrollArea, QGridLayout, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os, random
from core.settings import SettingsManager
from core.ffmpegworker import FFmpegWorkerManager
from core.thumbnails import ThumbnailWorker
from core.presets import PresetManagerDialog

class CollageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager.instance()
        self.input_folder = ""
        self.thumb_widgets = {}
        self.thumb_files = []
        self.thumbdir = os.path.expanduser("~/.megatool_thumbs")
        self.worker_manager = FFmpegWorkerManager()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.folder_label = QLabel("Geen map geselecteerd")
        self.select_btn = QPushButton("Selecteer map met video's")
        self.select_btn.clicked.connect(self.select_folder)

        folder_row = QHBoxLayout()
        folder_row.addWidget(self.select_btn)
        folder_row.addWidget(self.folder_label)

        self.shuffle_cb = QCheckBox("Random volgorde")
        self.transcode_cb = QCheckBox("Forceer transcodering")
        self.fade_cb = QCheckBox("Fade-in/out per clip")
        self.crossfade_cb = QCheckBox("Audio crossfades")

        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(5, 600)
        self.duration_spin.setValue(120)
        self.duration_label = QLabel("Collage duur (s):")

        dur_row = QHBoxLayout()
        dur_row.addWidget(self.duration_label)
        dur_row.addWidget(self.duration_spin)

        self.load_preset_btn = QPushButton("Laad preset")
        self.start_btn = QPushButton("Start Collage")
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setEnabled(False)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.load_preset_btn)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.cancel_btn)

        self.progress = QProgressBar()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        self.thumb_area = QScrollArea()
        self.thumb_grid = QGridLayout()
        thumb_widget = QWidget()
        thumb_widget.setLayout(self.thumb_grid)
        self.thumb_area.setWidget(thumb_widget)
        self.thumb_area.setWidgetResizable(True)
        self.thumb_area.setFixedHeight(140)

        layout.addLayout(folder_row)
        layout.addWidget(self.thumb_area)
        for w in (self.shuffle_cb, self.transcode_cb, self.fade_cb, self.crossfade_cb):
            layout.addWidget(w)
        layout.addLayout(dur_row)
        layout.addLayout(btn_row)
        layout.addWidget(QLabel("Voortgang:"))
        layout.addWidget(self.progress)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_output)

        self.load_preset_btn.clicked.connect(lambda: self.load_preset())
        self.start_btn.clicked.connect(self.create_collage)
        self.cancel_btn.clicked.connect(self._on_cancel)
        self.setAcceptDrops(True)

    def set_terminal(self, log_func):
        self.log = log_func

    def log(self, msg):
        self.log_output.append(msg)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def select_folder(self):
        fld = QFileDialog.getExistingDirectory(self, "Selecteer videomap")
        if fld:
            self.input_folder = fld
            self.folder_label.setText(fld)
            self.log(f"📁 Geselecteerd: {fld}")
            self.update_thumbnails()

    def update_thumbnails(self):
        while self.thumb_grid.count():
            w = self.thumb_grid.takeAt(0).widget()
            if w:
                w.deleteLater()
        if not self.input_folder or not os.path.exists(self.input_folder):
            return
        files = [
            os.path.join(self.input_folder, f) for f in os.listdir(self.input_folder)
            if f.lower().endswith((".mp4", ".avi", ".mkv", ".mov", ".webm"))
        ]
        if not files:
            return
        self.thumb_files = files
        self.thumb_widgets = {}
        self.thumb_worker = ThumbnailWorker(files, self.thumbdir)
        self.thumb_worker.thumbReady.connect(self._add_thumbnail)
        self.thumb_worker.start()

    def _add_thumbnail(self, filepath, thumbpath):
        row = len(self.thumb_widgets) // 6
        col = len(self.thumb_widgets) % 6
        lbl = QLabel()
        lbl.setFixedSize(160, 90)
        lbl.setFrameShape(QFrame.Shape.Box)
        pix = QPixmap(thumbpath)
        lbl.setPixmap(pix.scaled(160, 90, Qt.AspectRatioMode.KeepAspectRatio))
        lbl.setToolTip(os.path.basename(filepath))
        self.thumb_grid.addWidget(lbl, row, col)
        self.thumb_widgets[filepath] = lbl

    def _on_cancel(self):
        self.worker_manager.cancel()

    def load_preset(self):
        dlg = PresetManagerDialog(self, self.settings.get("presets_dir"), None)
        res = dlg.exec()
        if res == 1 and dlg.selected:
            self.log(f"✅ Preset '{dlg.selected}' geladen.")

    def create_collage(self):
        if not self.input_folder:
            self.log("❌ Geen map geselecteerd.", level="error")
            return
        self.log("🚧 Collage generatie nog niet geïmplementeerd.")
