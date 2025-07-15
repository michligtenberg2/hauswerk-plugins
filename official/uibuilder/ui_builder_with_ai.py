from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QFrame, QListWidget, QListWidgetItem, QInputDialog
)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag

class DroppableCell(QFrame):
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setFrameShape(QFrame.Shape.Box)
        self.setFixedHeight(80)
        self.setAcceptDrops(True)
        self.label = QLabel("↳ Drop of klik", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #f4f4f4;")
        self.mousePressEvent = self.choose_widget

    def choose_widget(self, event):
        items = ["QLabel", "QCheckBox", "QSlider", "QPushButton", "QProgressBar", "QTextEdit"]
        item, ok = QInputDialog.getItem(self, "Widget kiezen", "Selecteer widget:", items, 0, False)
        if ok and item:
            self.set_widget(item)

    def set_widget(self, name):
        self.label.setText(name)
        self.setStyleSheet("background-color: #d9f9d9;")

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        widget_name = event.mimeData().text()
        self.set_widget(widget_name)
        event.acceptProposedAction()

class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)

    def startDrag(self, supported_actions):
        item = self.currentItem()
        if item:
            mime = QMimeData()
            mime.setText(item.text())
            drag = QDrag(self)
            drag.setMimeData(mime)
            drag.exec()

class UIBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI Builder")
        self.grid_rows = 6
        self.grid_cols = 2
        self.init_ui()

    def init_ui(self):
        self.toolbox = DraggableListWidget()
        self.toolbox.setFixedWidth(200)
        for widget_name in ["QLabel", "QCheckBox", "QSlider", "QPushButton", "QProgressBar", "QTextEdit"]:
            self.toolbox.addItem(QListWidgetItem(widget_name))

        self.canvas = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(8)
        self.canvas.setLayout(self.grid_layout)

        self.cells = {}
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell = DroppableCell(r, c)
                self.grid_layout.addWidget(cell, r, c)
                self.cells[(r, c)] = cell

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.toolbox)
        main_layout.addWidget(self.canvas)
        self.setLayout(main_layout)


    def export_plugin(self, plugin_name="GeneratedPlugin"):
        lines = [
            "from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QSlider, QTextEdit, QProgressBar",
            "from PyQt6.QtCore import Qt",
            "",
            f"class {plugin_name}(QWidget):",
            "    def __init__(self):",
            "        super().__init__()",
            f"        self.setWindowTitle('{plugin_name}')",
            "        layout = QVBoxLayout()"
        ]

        # Loop door canvas en voeg widgets toe in volgorde
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell = self.cells[(r, c)]
                widget = cell.label.text().strip()
                if widget.startswith("Q"):
                    var = widget.lower()
                    lines.append(f"        self.{var}_{r}_{c} = {widget}()")
                    if widget == "QLabel":
                        lines.append(f"        self.{var}_{r}_{c}.setText('Label {r},{c}')")
                    if widget == "QTextEdit":
                        lines.append(f"        self.{var}_{r}_{c}.setReadOnly(True)")
                    lines.append(f"        layout.addWidget(self.{var}_{r}_{c})")

        lines.append("        self.setLayout(layout)")

        # Save to file
        from pathlib import Path
        path = Path(__file__).parent / "widgets"
        path.mkdir(exist_ok=True)
        fpath = path / f"{plugin_name.lower()}.py"
        with open(fpath, "w") as f:
            f.write("\n".join(lines))

        print(f"✅ Plugin opgeslagen als: {fpath}")

# Voor test:
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout
    import sys
    app = QApplication(sys.argv)
    window = UIBuilder()
    layout = QVBoxLayout()
    layout.addWidget(window)
    export_btn = QPushButton("Genereer plugin")
    export_btn.clicked.connect(lambda: window.export_plugin("CanvasPlugin"))
    layout.addWidget(export_btn)
    container = QWidget()
    container.setLayout(layout)
    container.setWindowTitle("Hauswerk UI Builder (Testmode)")
    container.resize(800, 600)
    container.show()
    sys.exit(app.exec())


    def save_layout_to_json(self, filename="layout.json"):
        layout_data = []
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell = self.cells[(r, c)]
                widget = cell.label.text().strip()
                layout_data.append({
                    "row": r,
                    "col": c,
                    "widget": widget if widget.startswith("Q") else ""
                })
        from pathlib import Path
        fpath = Path(__file__).parent / filename
        with open(fpath, "w") as f:
            json.dump(layout_data, f, indent=2)
        print(f"💾 Layout opgeslagen als {fpath}")

    def load_layout_from_json(self, filename="layout.json"):
        from pathlib import Path
        fpath = Path(__file__).parent / filename
        if not fpath.exists():
            print("⚠️ Layoutbestand niet gevonden.")
            return
        with open(fpath, "r") as f:
            layout_data = json.load(f)
        for item in layout_data:
            r, c = item["row"], item["col"]
            widget = item.get("widget", "")
            if widget and widget.startswith("Q"):
                self.cells[(r, c)].set_widget(widget)

# Aanpassen testvenster om knoppen toe te voegen
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout
    import sys
    app = QApplication(sys.argv)
    window = UIBuilder()

    # Extra knoppen
    export_btn = QPushButton("Genereer plugin")
    save_btn = QPushButton("Sla layout op")
    load_btn = QPushButton("Laad layout")

    export_btn.clicked.connect(lambda: window.export_plugin("CanvasPlugin"))
    save_btn.clicked.connect(lambda: window.save_layout_to_json("layout.json"))
    load_btn.clicked.connect(lambda: window.load_layout_from_json("layout.json"))

    button_row = QHBoxLayout()
    button_row.addWidget(export_btn)
    button_row.addWidget(save_btn)
    button_row.addWidget(load_btn)

    layout = QVBoxLayout()
    layout.addWidget(window)
    layout.addLayout(button_row)

    container = QWidget()
    container.setLayout(layout)
    container.setWindowTitle("Hauswerk UI Builder (met layout save/load)")
    container.resize(900, 640)
    container.show()
    sys.exit(app.exec())


    def update_live_preview(self):
        from PyQt6.QtWidgets import QLabel, QCheckBox, QSlider, QPushButton, QTextEdit, QProgressBar, QVBoxLayout
        # Verwijder oude preview
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell = self.cells[(r, c)]
                widget = cell.label.text().strip()
                if widget == "QLabel":
                    lbl = QLabel("Voorbeeld Label")
                    self.preview_layout.addWidget(lbl)
                elif widget == "QCheckBox":
                    cb = QCheckBox("Voorbeeld Checkbox")
                    self.preview_layout.addWidget(cb)
                elif widget == "QSlider":
                    sld = QSlider(Qt.Orientation.Horizontal)
                    self.preview_layout.addWidget(sld)
                elif widget == "QPushButton":
                    btn = QPushButton("Voorbeeld Knop")
                    self.preview_layout.addWidget(btn)
                elif widget == "QTextEdit":
                    txt = QTextEdit("Logvenster voorbeeld")
                    txt.setReadOnly(True)
                    self.preview_layout.addWidget(txt)
                elif widget == "QProgressBar":
                    p = QProgressBar()
                    p.setValue(42)
                    self.preview_layout.addWidget(p)

    def set_widget(self, r, c, name):
        self.cells[(r, c)].set_widget(name)
        self.update_live_preview()

    # Override cell set_widget to call preview update
    DroppableCell.set_widget = lambda self, name: (
        setattr(self.label, 'text', name),
        self.setStyleSheet("background-color: #d9f9d9;"),
        self.parent().update_live_preview()
    )[0]  # Return None

# Inject preview area into layout
# Overwrite init_ui to add preview panel
old_init_ui = UIBuilder.init_ui
def new_init_ui(self):
    old_init_ui(self)
    from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFrame
    preview_wrapper = QVBoxLayout()
    preview_title = QLabel("🔍 Live Preview")
    preview_title.setStyleSheet("font-weight: bold; padding: 4px;")
    self.preview_panel = QFrame()
    self.preview_panel.setFrameShape(QFrame.Shape.Box)
    self.preview_layout = QVBoxLayout(self.preview_panel)
    preview_wrapper.addWidget(preview_title)
    preview_wrapper.addWidget(self.preview_panel)
    self.layout().addLayout(preview_wrapper)

UIBuilder.init_ui = new_init_ui


    def update_live_preview(self):
        from PyQt6.QtWidgets import QLabel, QCheckBox, QSlider, QPushButton, QTextEdit, QProgressBar, QVBoxLayout
        # Leeg oude preview netjes
        for i in reversed(range(self.preview_layout.count())):
            item = self.preview_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        seen = set()
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell = self.cells[(r, c)]
                widget = cell.label.text().strip()
                if widget.startswith("Q") and (r, c) not in seen:
                    seen.add((r, c))
                    if widget == "QLabel":
                        w = QLabel("Voorbeeld Label")
                    elif widget == "QCheckBox":
                        w = QCheckBox("Voorbeeld Checkbox")
                    elif widget == "QSlider":
                        w = QSlider(Qt.Orientation.Horizontal)
                    elif widget == "QPushButton":
                        w = QPushButton("Voorbeeld Knop")
                    elif widget == "QTextEdit":
                        w = QTextEdit("Logvenster voorbeeld")
                        w.setReadOnly(True)
                    elif widget == "QProgressBar":
                        w = QProgressBar()
                        w.setValue(42)
                    else:
                        continue
                    w.setStyleSheet("margin: 4px;")
                    self.preview_layout.addWidget(w)

        self.preview_panel.setStyleSheet("background-color: #ffffff; padding: 8px;")



    def export_plugin(self, plugin_name="CanvasPlugin"):
        lines = [
            "from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QSlider, QTextEdit, QProgressBar",
            "from PyQt6.QtCore import Qt",
            "",
            f"class {plugin_name}(QWidget):",
            "    def __init__(self):",
            "        super().__init__()",
            f"        self.setWindowTitle('{plugin_name}')",
            "        layout = QVBoxLayout()"
        ]

        added = False
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell = self.cells[(r, c)]
                widget = cell.label.text().strip()
                if widget.startswith("Q"):
                    var = widget.lower()
                    lines.append(f"        self.{var}_{r}_{c} = {widget}()")
                    if widget == "QLabel":
                        lines.append(f"        self.{var}_{r}_{c}.setText('Label {r},{c}')")
                    if widget == "QTextEdit":
                        lines.append(f"        self.{var}_{r}_{c}.setReadOnly(True)")
                    lines.append(f"        layout.addWidget(self.{var}_{r}_{c})")
                    added = True

        if not added:
            print("⚠️ Lege plugin. Geen widgets om te exporteren.")
            return

        lines.append("        self.setLayout(layout)")

        from pathlib import Path
        path = Path(__file__).parent / "widgets"
        path.mkdir(exist_ok=True)
        fpath = path / f"{plugin_name.lower()}.py"
        with open(fpath, "w") as f:
            f.write("\n".join(lines))

        print(f"✅ Plugin gegenereerd: {fpath}")


from PyQt6.QtWidgets import QLineEdit, QMessageBox

def new_init_ui(self):
    old_init_ui(self)
    # Pluginnaam invoerveld boven knoppen
    self.plugin_name_input = QLineEdit("CanvasPlugin")
    self.plugin_name_input.setPlaceholderText("Voer pluginnaam in...")
    self.layout().insertWidget(0, self.plugin_name_input)

UIBuilder.init_ui = new_init_ui

# Pas export_plugin aan om naam uit invoerveld te halen
def export_with_name(self):
    name = self.plugin_name_input.text().strip()
    if not name or any(c in name for c in " ./\\:;"):
        QMessageBox.warning(self, "Fout", "Ongeldige pluginnaam.")
        return
    self.export_plugin(plugin_name=name)

UIBuilder.export_with_name = export_with_name

# Update test-launcher om nieuwe functie te gebruiken
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout
    import sys
    app = QApplication(sys.argv)
    window = UIBuilder()

    export_btn = QPushButton("Genereer plugin")
    save_btn = QPushButton("Sla layout op")
    load_btn = QPushButton("Laad layout")

    export_btn.clicked.connect(lambda: window.export_with_name())
    save_btn.clicked.connect(lambda: window.save_layout_to_json("layout.json"))
    load_btn.clicked.connect(lambda: window.load_layout_from_json("layout.json"))

    button_row = QHBoxLayout()
    button_row.addWidget(export_btn)
    button_row.addWidget(save_btn)
    button_row.addWidget(load_btn)

    layout = QVBoxLayout()
    layout.addWidget(window)
    layout.addLayout(button_row)

    container = QWidget()
    container.setLayout(layout)
    container.setWindowTitle("Hauswerk UI Builder (met pluginnaam en waarschuwingen)")
    container.resize(900, 680)
    container.show()
    sys.exit(app.exec())


from PyQt6.QtWidgets import QTextEdit

def new_init_ui_with_preview(self):
    new_init_ui(self)
    self.code_preview = QTextEdit()
    self.code_preview.setReadOnly(True)
    self.code_preview.setStyleSheet("background-color: #f8f8f8; font-family: monospace; font-size: 11px;")
    self.layout().insertWidget(1, self.code_preview)

UIBuilder.init_ui = new_init_ui_with_preview

# Update export_plugin om code ook te tonen in previewvenster
def export_plugin_and_preview(self, plugin_name="CanvasPlugin"):
    lines = [
        "from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QSlider, QTextEdit, QProgressBar",
        "from PyQt6.QtCore import Qt",
        "",
        f"class {plugin_name}(QWidget):",
        "    def __init__(self):",
        "        super().__init__()",
        f"        self.setWindowTitle('{plugin_name}')",
        "        layout = QVBoxLayout()"
    ]

    added = False
    for r in range(self.grid_rows):
        for c in range(self.grid_cols):
            cell = self.cells[(r, c)]
            widget = cell.label.text().strip()
            if widget.startswith("Q"):
                var = widget.lower()
                lines.append(f"        self.{var}_{r}_{c} = {widget}()")
                if widget == "QLabel":
                    lines.append(f"        self.{var}_{r}_{c}.setText('Label {r},{c}')")
                if widget == "QTextEdit":
                    lines.append(f"        self.{var}_{r}_{c}.setReadOnly(True)")
                lines.append(f"        layout.addWidget(self.{var}_{r}_{c})")
                added = True

    if not added:
        QMessageBox.warning(self, "Fout", "Geen widgets aanwezig om te exporteren.")
        return

    lines.append("        self.setLayout(layout)")
    from pathlib import Path
    path = Path(__file__).parent / "widgets"
    path.mkdir(exist_ok=True)
    fpath = path / f"{plugin_name.lower()}.py"
    with open(fpath, "w") as f:
        f.write("\n".join(lines))

    # Toon in code preview
    self.code_preview.setPlainText("\n".join(lines))
    print(f"✅ Plugin gegenereerd: {fpath}")

UIBuilder.export_plugin = export_plugin_and_preview


from PyQt6.QtWidgets import QLineEdit, QMessageBox, QInputDialog
from core.ai_assist import suggest_layout

def apply_ai_layout(self):
    prompt, ok = QInputDialog.getText(self, "AI Plugin Assistent", "Wat wil je bouwen?")
    if ok and prompt:
        layout = suggest_layout(prompt)
        for item in layout:
            r, c = item["row"], item["col"]
            widget = item["widget"]
            if (r, c) in self.cells:
                self.cells[(r, c)].set_widget(widget)
        self.update_live_preview()

UIBuilder.apply_ai_layout = apply_ai_layout

# Voeg knop toe onderaan test-launcher
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout
    import sys
    app = QApplication(sys.argv)
    window = UIBuilder()

    export_btn = QPushButton("Genereer plugin")
    save_btn = QPushButton("Sla layout op")
    load_btn = QPushButton("Laad layout")
    ai_btn = QPushButton("✨ AI-suggestie")

    export_btn.clicked.connect(lambda: window.export_with_name())
    save_btn.clicked.connect(lambda: window.save_layout_to_json("layout.json"))
    load_btn.clicked.connect(lambda: window.load_layout_from_json("layout.json"))
    ai_btn.clicked.connect(lambda: window.apply_ai_layout())

    button_row = QHBoxLayout()
    button_row.addWidget(export_btn)
    button_row.addWidget(save_btn)
    button_row.addWidget(load_btn)
    button_row.addWidget(ai_btn)

    layout = QVBoxLayout()
    layout.addWidget(window)
    layout.addLayout(button_row)

    container = QWidget()
    container.setLayout(layout)
    container.setWindowTitle("Hauswerk UI Builder + AI")
    container.resize(960, 700)
    container.show()
    sys.exit(app.exec())
