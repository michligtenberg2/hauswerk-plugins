# widgets/stretcher.py

import os
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog,
    QComboBox, QCheckBox, QTextEdit, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from widgets.standard_tool_layout import StandardToolLayout

class VideoStretchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Video Stretch Tool")

        self.input_label = QLabel("Geen bestand geselecteerd")
        self.select_btn = QPushButton("Selecteer video")
        self.factor_label = QLabel("Vertraag factor:")
        self.factor_dropdown = QComboBox()
        self.factor_dropdown.addItems(["2", "4", "8"])
        self.audio_checkbox = QCheckBox("Audio meevertragen")
        self.start_btn = QPushButton("Start verwerking")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.input_path = ""

        # --- Layout rows ---
        input_hbox = QHBoxLayout()
        input_hbox.addWidget(self.input_label)
        input_hbox.addWidget(self.select_btn)

        factor_hbox = QHBoxLayout()
        factor_hbox.addWidget(self.factor_label)
        factor_hbox.addWidget(self.factor_dropdown)
        factor_hbox.addWidget(self.audio_checkbox)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.start_btn)

        # Layout alles via StandardToolLayout
        self.layout_widget = StandardToolLayout(
            input_row=input_hbox,
            option_rows=[factor_hbox],
            button_row=btn_hbox,
            log_widget=self.log_output
        )
        self.setLayout(self.layout_widget.layout())

        self.select_btn.clicked.connect(self.select_file)
        self.start_btn.clicked.connect(self.process_video)

    def log(self, message):
        self.log_output.append(message)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecteer video", "", "Video Files (*.mp4 *.mov *.avi)")
        if path:
            self.input_path = path
            self.input_label.setText(os.path.basename(path))
            self.log(f"🎞️ Geselecteerd: {path}")

    def process_video(self):
        if not self.input_path:
            QMessageBox.warning(self, "Fout", "Geen videobestand geselecteerd.")
            return

        factor = int(self.factor_dropdown.currentText())
        stretch_factor = float(factor)
        audio = self.audio_checkbox.isChecked()

        base, ext = os.path.splitext(self.input_path)
        output_file = f"{base}_x{factor}{ext}"

        if audio:
            if factor == 2:
                atempo = "atempo=0.5"
            elif factor == 4:
                atempo = "atempo=0.5,atempo=0.5"
            elif factor == 8:
                atempo = "atempo=0.5,atempo=0.5,atempo=0.5"
            else:
                QMessageBox.warning(self, "Ongeldig", "Alleen x2, x4, x8 ondersteund voor audio.")
                return

            cmd = [
                "ffmpeg", "-y", "-i", self.input_path,
                "-filter_complex",
                f"[0:v]setpts={stretch_factor}*PTS[v];[0:a]{atempo}[a]",
                "-map", "[v]", "-map", "[a]", output_file
            ]
        else:
            cmd = [
                "ffmpeg", "-y", "-i", self.input_path,
                "-filter:v", f"setpts={stretch_factor}*PTS",
                "-an", output_file
            ]

        self.log(f"🚀 Start verwerking naar {output_file}...")
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.log(f"✅ Klaar: {output_file}")
        except subprocess.CalledProcessError:
            self.log(f"❌ Fout tijdens verwerken van video.")
