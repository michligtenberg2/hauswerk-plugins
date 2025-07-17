"""Psychotisch video mashup plugin for Hauswerk."""

import os
import random
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QTextEdit, QSpinBox, QLineEdit,
    QFileDialog, QProgressBar, QVBoxLayout, QHBoxLayout
)

class PsychotischTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._connect_signals()
        self.input_folder = ""
        self.output_path = ""

    def _init_ui(self):
        self.select_btn = QPushButton("Selecteer map met video's")
        self.folder_label = QLabel("Geen map geselecteerd")
        self.output_btn = QPushButton("Kies output-bestand")
        self.output_label = QLabel("Geen export-bestand gekozen")
        self.dur_label = QLabel("Totale duur (seconden):")
        self.dur_spin = QSpinBox()
        self.dur_spin.setRange(5, 9999)
        self.dur_spin.setValue(60)
        self.bpm_label = QLabel("BPM (voor cut-ritme):")
        self.bpm_input = QLineEdit("120")
        self.size_label = QLabel("Output resolutie (breedte x hoogte, bijv 720x540):")
        self.size_input = QLineEdit("720x540")
        self.min_layer_label = QLabel("Min. lagen tegelijk:")
        self.min_layer_spin = QSpinBox()
        self.min_layer_spin.setRange(1, 10)
        self.min_layer_spin.setValue(1)
        self.max_layer_label = QLabel("Max. lagen tegelijk:")
        self.max_layer_spin = QSpinBox()
        self.max_layer_spin.setRange(1, 10)
        self.max_layer_spin.setValue(3)
        self.start_btn = QPushButton("Start Psychotische Mix")
        self.progress = QProgressBar()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout = QVBoxLayout(self)
        for w in (
            self.select_btn, self.folder_label,
            self.output_btn, self.output_label,
            self.dur_label, self.dur_spin,
            self.bpm_label, self.bpm_input,
            self.size_label, self.size_input,
            self.min_layer_label, self.min_layer_spin,
            self.max_layer_label, self.max_layer_spin,
            self.start_btn, QLabel("Voortgang:"), self.progress,
            QLabel("Log:"), self.log_output
        ):
            layout.addWidget(w)

    def _connect_signals(self):
        self.select_btn.clicked.connect(self.select_folder)
        self.output_btn.clicked.connect(self.select_output)
        self.start_btn.clicked.connect(self.run_psychotisch)

    def log(self, msg):
        self.log_output.append(str(msg))

    def select_folder(self):
        fld = QFileDialog.getExistingDirectory(self, "Selecteer videomap")
        if fld:
            self.input_folder = fld
            self.folder_label.setText(fld)
            self.log(f"📁 Geselecteerd: {fld}")

    def select_output(self):
        out_path, _ = QFileDialog.getSaveFileName(self, "Kies output-bestand", "", "MP4 Video (*.mp4)")
        if out_path:
            self.output_path = out_path
            self.output_label.setText(f"{out_path}")
            self.log(f"💾 Export-bestand gekozen: {out_path}")

    def run_psychotisch(self):
        if not self.input_folder or not os.path.isdir(self.input_folder):
            self.log("❌ Geen map geselecteerd.")
            return
        if not self.output_path:
            self.log("❌ Geen export-bestand gekozen.")
            return

        total_duration = self.dur_spin.value()
        bpm = int(self.bpm_input.text()) if self.bpm_input.text().isdigit() else 120
        size = self.size_input.text().strip() or "720x540"
        min_layers = self.min_layer_spin.value()
        max_layers = self.max_layer_spin.value()
        # Start als subprocess zodat je GUI niet blokkeert (optioneel: doe threading)
        self.make_psychotisch_video(
            self.input_folder, self.output_path, total_duration, bpm,
            self.log, self.progress.setValue, size, min_layers, max_layers
        )

    def make_psychotisch_video(
        self, folder, output_path, total_duration, bpm=120, log=print,
        progress=lambda v: None, size="720x540", min_layers=1, max_layers=3
    ):
        w, h = [int(i) for i in size.lower().replace(" ", "").split('x')]
        cuts_per_beat = random.randint(2, 7)
        frag_len = 60.0 / bpm / cuts_per_beat
        num_frags = int(total_duration / frag_len)
        files = [f for f in os.listdir(folder) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm', '.wmv'))]
        if not files:
            log("❌ Geen videobestanden gevonden.")
            return

        log(f"🧠 Super-Psychotisch: {num_frags} frags ({frag_len:.2f}s p. stuk, {cuts_per_beat} cuts/beat)")
        frags = []
        concatlist = os.path.join(folder, "_psych_concat.txt")
        for i in range(num_frags):
            n_layers = random.randint(min_layers, max_layers)
            vids = random.sample(files, n_layers)
            filters = []
            inputs = []
            overlay_labels = []
            audio_filters = []
            for idx, vf in enumerate(vids):
                vpath = os.path.join(folder, vf)
                label = f"v{idx}"
                start = random.uniform(0, 1)
                fx = [f"scale={w}:{h}:force_original_aspect_ratio=decrease"]
                if random.random() < 0.7: fx.append("crop=w=iw/1.2:h=ih/1.2:x=rand(1)*iw/8:y=rand(1)*ih/8")
                if random.random() < 0.4: fx.append("hflip")
                if random.random() < 0.3: fx.append("vflip")
                if random.random() < 0.4: fx.append(f"hue=s={random.uniform(0.5,3):.2f}:H={random.randint(0,180)}")
                if random.random() < 0.2: fx.append("negate")
                if random.random() < 0.3: fx.append(f"eq=contrast={random.uniform(0.7,2.0):.2f}:saturation={random.uniform(1,3):.2f}")
                if random.random() < 0.25: fx.append(f"rotate={random.uniform(-0.5,0.5):.2f}")
                if random.random() < 0.2: fx.append("fade=t=in:st=0:d=0.03:alpha=1,fade=t=out:st=0.18:d=0.03:alpha=1")
                if random.random() < 0.2: fx.append("tblend=all_mode=addition")
                filters.append(f"[{idx}:v]{','.join(fx)}[{label}]")
                overlay_labels.append(label)
                # Audio fx per layer
                afx = []
                if random.random() < 0.3: afx.append(f"atempo={random.uniform(0.8,1.25):.2f}")
                if random.random() < 0.15: afx.append(f"rubberband=tempo={random.uniform(0.7,1.3):.2f}")
                if random.random() < 0.2: afx.append(f"adelay={random.randint(0,200)}|{random.randint(0,200)}")
                if random.random() < 0.4: afx.append(f"pan=stereo|c0=c0|c1=c1")
                if random.random() < 0.35: afx.append("volume=0.8")
                if afx:
                    audio_filters.append(f"[{idx}:a]{','.join(afx)}[a{idx}]")
                else:
                    audio_filters.append(f"[{idx}:a]anull[a{idx}]")
                inputs.append(f'-ss {start:.2f} -t {frag_len:.2f} -i "{vpath}"')
            # Overlay chain
            ol = f"[{overlay_labels[0]}]"
            for j in range(1, n_layers):
                x = random.randint(-60, 60)
                y = random.randint(-60, 60)
                alpha = random.uniform(0.3, 0.8)
                blend = "addition" if random.random() < 0.5 else "overlay"
                ol = f"{ol}[{overlay_labels[j]}]overlay=shortest=1:x={x}:y={y}:alpha={alpha}:{'format=auto' if blend=='overlay' else 'format=rgb'}[ol{j}]"
                ol = f"[ol{j}]"
            # Final filter chain
            full_vf = ";".join(filters + [ol.replace('[ol'+str(n_layers-1)+']','[vout]')])
            amix = f"{''.join([f'[a{k}]' for k in range(n_layers)])}amix=inputs={n_layers}:duration=shortest[aout]"
            out = os.path.join(folder, f"_psych_{i:04d}.mp4")
            cmd = (
                f'ffmpeg -y -hide_banner -loglevel error '
                f'{" ".join(inputs)} -filter_complex "{full_vf};{";".join(audio_filters)};{amix}" '
                f'-map "[vout]" -map "[aout]" -c:v libx264 -preset ultrafast -crf 20 -c:a aac -b:a 192k -movflags +faststart "{out}"'
            )
            log(f"🎬 [{i+1}/{num_frags}] {os.path.basename(out)} ({n_layers} lagen, {frag_len:.2f}s)")
            try:
                subprocess.run(cmd, shell=True, check=True)
                frags.append(out)
            except Exception as e:
                log(f"⚠️ Fout bij fragment: {e}")
            progress(int(100 * (i+1)/num_frags))
        # Maak concat list
        with open(concatlist, "w") as f:
            for frag in frags:
                f.write(f"file '{frag}'\n")
        log(f"▶️ Concat alle psycho-fragmenten...")
        cmd_concat = (
            f'ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i "{concatlist}" '
            f'-c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k -movflags +faststart "{output_path}"'
        )
        try:
            subprocess.run(cmd_concat, shell=True, check=True)
            log(f"✅ Psychotisch concat voltooid! Output: {output_path}")
        except Exception as e:
            log(f"❌ Fout bij concat: {e}")
        progress(100)
        # Cleanup
        for frag in frags:
            try: os.remove(frag)
            except: pass
        try: os.remove(concatlist)
        except: pass

# Alias for Hauswerk loader
class PluginWidget(PsychotischTab):
    """Entry point for Hauswerk."""
    pass

