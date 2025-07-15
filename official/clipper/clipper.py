# clipper_widget.py (gestylede versie)
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QTextEdit,
    QSpinBox, QFileDialog, QProgressBar
)
from PyQt6.QtCore import Qt
import os

class RandomClipperWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.input_file = ""
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.file_label = QLabel("Geen bestand geselecteerd")
        self.input_btn = QPushButton("Selecteer video")
        self.input_btn.clicked.connect(self.select_file)

        file_row = QHBoxLayout()
        file_row.addWidget(self.input_btn)
        file_row.addWidget(self.file_label)

        self.min_spin = QSpinBox()
        self.min_spin.setRange(1, 60)
        self.min_spin.setValue(5)
        self.max_spin = QSpinBox()
        self.max_spin.setRange(1, 300)
        self.max_spin.setValue(15)

        self.transcode_cb = QCheckBox("Forceer transcodering")

        dur_row = QHBoxLayout()
        dur_row.addWidget(QLabel("Min duur:"))
        dur_row.addWidget(self.min_spin)
        dur_row.addWidget(QLabel("Max duur:"))
        dur_row.addWidget(self.max_spin)
        dur_row.addWidget(self.transcode_cb)

        self.clip_btn = QPushButton("Genereer clips")
        self.clip_btn.clicked.connect(self.create_clips)

        self.progress = QProgressBar()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        layout.addLayout(file_row)
        layout.addLayout(dur_row)
        layout.addWidget(self.clip_btn)
        layout.addWidget(self.progress)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_output)

    def set_terminal(self, log_fn):
        self.log = log_fn

    def log(self, msg):
        self.log_output.append(msg)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecteer video", "", "Video Files (*.mp4 *.mov *.avi)")
        if file:
            self.input_file = file
            self.file_label.setText(os.path.basename(file))
            self.log(f"🎞️ Geselecteerd: {file}")

    def create_clips(self):
        if not self.input_file:
            self.log("❌ Geen videobestand geselecteerd.")
            return
        self.log("🚧 Clip generatie nog niet geïmplementeerd.")
