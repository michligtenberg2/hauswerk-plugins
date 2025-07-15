import sys
import os
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QRect
from importlib.util import spec_from_file_location, module_from_spec

plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "official"))
app = QApplication([])

for folder in os.listdir(plugins_dir):
    path = os.path.join(plugins_dir, folder)
    if not os.path.isdir(path):
        continue
    metadata_path = os.path.join(path, "metadata.json")
    if not os.path.exists(metadata_path):
        continue
    try:
        with open(metadata_path) as f:
            meta = json.load(f)
    except:
        continue

    entry = meta.get("entry", "main.py")
    class_name = meta.get("class", None)
    preview_path = os.path.join(path, "preview.jpg")

    if not class_name:
        print(f"⏭️  {folder}: geen class opgegeven")
        continue

    entry_path = os.path.join(path, entry)
    if not os.path.exists(entry_path):
        print(f"❌ {folder}: {entry} bestaat niet")
        continue

    try:
        spec = spec_from_file_location("plugin_module", entry_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        cls = getattr(module, class_name)
        widget = cls()
        widget.resize(800, 600)
        widget.show()
        app.processEvents()
        pixmap = QPixmap(widget.size())
        widget.render(pixmap)
        pixmap.save(preview_path, "JPG")
        widget.close()
        print(f"✅ {folder}: preview.jpg gegenereerd")
    except Exception as e:
        print(f"⚠️  {folder}: fout bij preview genereren: {e}")

sys.exit()
