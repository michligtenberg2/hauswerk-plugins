import os
import random
import subprocess
import json
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QCheckBox, QTextEdit, QMessageBox, QSpinBox,
    QProgressBar, QInputDialog, QToolBar, QStatusBar, QDialog, QDialogButtonBox, QHBoxLayout, QLineEdit, QComboBox
)
from PyQt6.QtGui import QAction

# ——————————— FFmpegWorker ———————————
class FFmpegWorker(QThread):
    # Signalen voor voortgang, logging en afronding
    progress = pyqtSignal(int)            # voortgang (0–100)
    log      = pyqtSignal(str)            # logregels
    finished = pyqtSignal(bool, str)      # succes + out_path

    def __init__(self, commands):
        super().__init__()
        self.commands = commands          # lijst met shell commands (ffmpeg etc)
        self._cancel = False
        self._proc = None                 # actueel subprocess, indien actief

    def run(self):
        total = len(self.commands)
        for idx, cmd in enumerate(self.commands, start=1):
            if self._cancel:
                self.log.emit("⛔️ Taak geannuleerd")
                self.finished.emit(False, "")
                return
            self.log.emit(f"▶️ {cmd}")
            try:
                # Start subprocess: stdout/stderr worden live uitgelezen
                self._proc = subprocess.Popen(
                    cmd, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                while True:
                    if self._cancel and self._proc:
                        self._proc.terminate()  # Onderbreek ffmpeg direct
                        self.log.emit("⛔️ FFmpeg proces afgebroken.")
                        self.finished.emit(False, "")
                        return
                    line = self._proc.stderr.readline()  # lees ffmpeg-foutregels live
                    if not line:
                        break
                    self.log.emit(line.rstrip())
                self._proc.wait()  # wacht tot ffmpeg klaar
            except Exception as e:
                self.log.emit(f"❌ Fout in worker: {e}")
                self.finished.emit(False, "")
                return
            finally:
                self._proc = None
            if self._cancel:
                self.log.emit("⛔️ Taak geannuleerd tijdens wachten.")
                self.finished.emit(False, "")
                return
            if self._proc and self._proc.returncode != 0:
                self.log.emit(f"❌ Fout bij stap {idx}, code {self._proc.returncode}")
                self.finished.emit(False, "")
                return
            pct = int(idx/total * 100)
            self.progress.emit(pct)
        self.log.emit("✅ Alle stappen voltooid")
        self.finished.emit(True, self.commands[-1])

    def cancel(self):
        self._cancel = True
        if self._proc:
            try:
                self._proc.terminate()    # Probeer subprocess te stoppen
            except Exception:
                pass


# ——————————— ConcatWidget ———————————
class ConcatWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Initialiseer GUI-elementen voor concat-paneel
        self.folder_label   = QLabel("Geen map geselecteerd")
        self.select_btn     = QPushButton("Selecteer map met video's")
        self.shuffle_cb     = QCheckBox("Random volgorde")
        self.transcode_cb   = QCheckBox("Forceer transcodering")
        self.fade_cb        = QCheckBox("Fade-in/out per clip")
        self.crossfade_cb   = QCheckBox("Audio crossfades")
        self.start_btn      = QPushButton("Start Concat")
        self.cancel_btn     = QPushButton("Cancel")
        self.cancel_btn.setEnabled(False)
        self.progress       = QProgressBar()
        self.log_output     = QTextEdit()
        self.log_output.setReadOnly(True)
        self.input_folder   = ""
        self.worker         = None

        # Bouw verticale layout met alle knoppen en velden
        layout = QVBoxLayout(self)
        for w in (
            self.select_btn, self.folder_label,
            self.shuffle_cb, self.transcode_cb,
            self.fade_cb, self.crossfade_cb,
            self.start_btn, self.cancel_btn,
            QLabel("Voortgang:"), self.progress,
            QLabel("Log:"), self.log_output
        ):
            layout.addWidget(w)
        # Koppel knoppen aan functies
        self.select_btn.clicked.connect(self.select_folder)
        self.start_btn.clicked.connect(self.concatenate_videos)
        self.cancel_btn.clicked.connect(self._on_cancel)

    def log(self, msg):
        self.log_output.append(msg)
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    def select_folder(self):
        # Open dialoog voor folder-selectie
        fld = QFileDialog.getExistingDirectory(self, "Selecteer videomap")
        if fld:
            self.input_folder = fld
            self.folder_label.setText(fld)
            self.log(f"📁 Geselecteerd: {fld}")

    def concatenate_videos(self):
        # Controleer of er een map geselecteerd is
        if not self.input_folder:
            QMessageBox.warning(self, "Fout", "Geen map geselecteerd.")
            return
        # Verzamel alle videobestanden uit de map
        files = [
            f for f in os.listdir(self.input_folder)
            if f.lower().endswith((
                ".mp4", ".mov", ".avi", ".mkv", ".flv",
                ".wmv", ".webm", ".mpg", ".mpeg"
            ))
        ]
        if self.shuffle_cb.isChecked():
            random.shuffle(files)
            self.log("🔀 Volgorde gerandomized")

        cmd_list = []  # Lijst met ffmpeg commando's
        for idx, vid in enumerate(files, start=1):
            inp = os.path.join(self.input_folder, vid)
            tmp = os.path.join(self.input_folder, f"_tmp_{idx}.mp4")
            filters = []
            if self.fade_cb.isChecked():
                filters.append("fade=t=in:st=0:d=1,fade=t=out:st=duration-1:d=1")
            vf = f"-vf {','.join(filters)}" if filters else ""
            # Forceer transcodering indien gevraagd
            if any((self.transcode_cb.isChecked(),
                    self.fade_cb.isChecked(),
                    self.crossfade_cb.isChecked())):
                cmd = (
                    f'ffmpeg -y -i "{inp}" {vf} '
                    '-c:v libx264 -preset veryfast -crf 23 '
                    '-c:a aac -b:a 192k '
                    f'"{tmp}"'
                )
            else:
                cmd = f'ffmpeg -y -i "{inp}" -c copy "{tmp}"'
            cmd_list.append(cmd)

        # Bouw concat-lijst voor ffmpeg
        list_file = os.path.join(self.input_folder, "concat_list.txt")
        file_list = " ".join([f'"{os.path.join(self.input_folder, f"_tmp_{i}.mp4")}"' for i in range(1, len(files)+1)])
        # Correct ge-escaped printf commando voor bash
        printf_cmd = f'bash -c "printf \'file \\"%s\\"\n\' {file_list} > {list_file}"'
        concat_txt = ["ffmpeg -f concat -safe 0 -i " + list_file + " -c copy "
                      + os.path.join(self.input_folder, "concatenated_output.mp4")]
        # Start worker-thread met alle stappen, incl. opruimen
        self._start_worker(cmd_list + [
            printf_cmd,
        ] + concat_txt + [
            f"bash -c \"rm -f {' '.join(os.path.join(self.input_folder, f'_tmp_{i}.mp4') for i in range(1, len(files)+1))} {list_file}\""
        ])

    def _start_worker(self, cmds):
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress.setValue(0)
        self.worker = FFmpegWorker(cmds)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.log)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_cancel(self):
        if self.worker:
            self.worker.cancel()

    def _on_finished(self, success, _):
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        if success:
            self.log("🚀 Concatenatie voltooid")
        else:
            self.log("⚠️ Concatenatie gestopt of gefaald")

# ——————————— CollageWidget ———————————
class CollageWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Init GUI voor collage: video-mappen, instellingen
        self.folder_label   = QLabel("Geen map geselecteerd")
        self.select_btn     = QPushButton("Selecteer map met video's")
        self.shuffle_cb     = QCheckBox("Random volgorde")
        self.transcode_cb   = QCheckBox("Forceer transcodering")
        self.fade_cb        = QCheckBox("Fade-in/out per clip")
        self.crossfade_cb   = QCheckBox("Audio crossfades")
        self.duration_label = QLabel("Collage duur (s):")
        self.duration_spin  = QSpinBox()
        self.duration_spin.setRange(10, 600)
        self.duration_spin.setValue(120)
        self.load_preset_btn = QPushButton("Laad preset")
        self.start_btn       = QPushButton("Start Collage")
        self.cancel_btn      = QPushButton("Cancel")
        self.cancel_btn.setEnabled(False)
        self.progress        = QProgressBar()
        self.log_output      = QTextEdit()
        self.log_output.setReadOnly(True)
        self.input_folder    = ""
        self.worker          = None
        # Layout met controls, settings
        layout = QVBoxLayout(self)
        for w in (
            self.select_btn, self.folder_label, self.shuffle_cb,
            self.transcode_cb, self.fade_cb, self.crossfade_cb,
            self.duration_label, self.duration_spin,
            self.load_preset_btn, self.start_btn, self.cancel_btn,
            QLabel("Voortgang:"), self.progress,
            QLabel("Log:"), self.log_output
        ):
            layout.addWidget(w)
        # Knoppen verbinden
        self.select_btn.clicked.connect(self.select_folder)
        self.load_preset_btn.clicked.connect(self.load_preset)
        self.start_btn.clicked.connect(self.create_collage)
        self.cancel_btn.clicked.connect(self._on_cancel)

    def log(self, msg):
        self.log_output.append(msg)
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    def select_folder(self):
        # Selecteer inputmap
        fld = QFileDialog.getExistingDirectory(self, "Selecteer videomap")
        if fld:
            self.input_folder = fld
            self.folder_label.setText(fld)
            self.log(f"📁 Geselecteerd: {fld}")

    def create_collage(self):
        if not self.input_folder:
            QMessageBox.warning(self, "Fout", "Geen map geselecteerd.")
            return
        files = [
            f for f in os.listdir(self.input_folder)
            if f.lower().endswith((
                ".mp4", ".mov", ".avi", ".mkv", ".flv",
                ".wmv", ".webm", ".mpg", ".mpeg"
            ))
        ]
        if self.shuffle_cb.isChecked():
            random.shuffle(files)
            self.log("🔀 Volgorde gerandomized")
        max_layers = min(len(files), 6)
        self.progress.setMaximum(max_layers)
        self.progress.setValue(0)
        dur = self.duration_spin.value()
        preset = {"clips": [], "duration": dur}
        inputs, filters, volumes = [], [], []
        # Bouw presetstructuur en filtergraph
        for idx, vid in enumerate(files[:max_layers], start=0):
            self.progress.setValue(idx+1)
            self.log(f"📦 Laag {idx+1}: {vid}")
            path = os.path.join(self.input_folder, vid)
            scale = random.uniform(0.3, 0.6)
            x = random.randint(0, 400)
            y = random.randint(0, 300)
            rot = random.uniform(-0.3, 0.3)
            fade = random.uniform(0.5, 1.5)
            start = random.uniform(0, dur-2)
            preset["clips"].append({
                "file": vid, "scale": scale,
                "x": x, "y": y,
                "rotation": rot,
                "fade_in": fade,
                "start_time": start
            })
            inputs.append(f'-i "{path}"')
            vf = [
                f"scale=iw*{scale}:-1",
                f"rotate={rot}:c=green@1",
                "format=yuva420p"
            ]
            if self.fade_cb.isChecked():
                vf += [
                    f"fade=t=in:st=0:d={fade}:alpha=1",
                    f"fade=t=out:st={dur-1}:d=1:alpha=1"
                ]
            vf.append(f"setpts=PTS+{start}/TB")
            filters.append(f"[{idx}:v]{','.join(vf)}[v{idx}]")
            volumes.append(f"[{idx}:a]volume=1.0[a{idx}]")
        # Bouw video overlay-chain en audio-mix/fade
        chain = "[v0]"
        for i in range(1, len(filters)):
            xi = preset["clips"][i]["x"]
            yi = preset["clips"][i]["y"]
            chain = f"{chain}[v{i}]overlay=shortest=1:x={xi}:y={yi}"
            if i < len(filters)-1:
                chain = f"[{chain}]"
        if self.crossfade_cb.isChecked() and len(volumes) >= 2:
            audio_map = "[0:a][1:a]acrossfade=d=2[aout]"
        else:
            audio_map = "".join(volumes) + f"amix=inputs={len(volumes)}:duration=longest[aout]"
        fc = ";".join(filters + volumes + [chain, audio_map])
        inp_str = " ".join(inputs)
        out = os.path.join(self.input_folder, "collage_output.mp4")
        cmd = (
            f'ffmpeg {inp_str} -filter_complex "{fc}" '
            f'-map "{chain}" -map "[aout]" '
        )
        if self.transcode_cb.isChecked():
            cmd += '-c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 192k '
        cmd += f'-t {dur} -y "{out}"'
        self._start_worker([cmd])

    def _start_worker(self, cmds):
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.worker = FFmpegWorker(cmds)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.log)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_cancel(self):
        if self.worker:
            self.worker.cancel()
    def _on_finished(self, success, _):
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        if success:
            self.log("🚀 Collage gereed")
        else:
            self.log("⚠️ Collage gestopt of gefaald")
    def load_preset(self):
        if not self.input_folder:
            QMessageBox.warning(self, "Fout", "Geen map geselecteerd.")
            return
        fname, ok = QInputDialog.getText(self, "Preset kiezen", "Naam voor preset:")
        if not ok or not fname:
            return
        ppath = os.path.join(self.input_folder, f"{fname}.json")
        if not os.path.exists(ppath):
            self.log("❌ Geen preset gevonden.")
            return
        with open(ppath, "r") as f:
            preset = json.load(f)
        self.duration_spin.setValue(preset.get("duration", 120))
        self.create_collage()

# ——————————— MegaTool (MainWindow) ———————————
class SettingsDialog(QDialog):
    SETTINGS_FILE = os.path.expanduser("~/.megatool_settings.json")
    def __init__(self, parent=None):
        super
