import os
import zipfile
import json

source_dir = "plugin_zips"   # Map met ZIP-bestanden
target_dir = "plugins"       # Doelmap waar plugins worden uitgepakt

os.makedirs(target_dir, exist_ok=True)

for filename in os.listdir(source_dir):
    if filename.endswith(".zip"):
        zip_path = os.path.join(source_dir, filename)
        plugin_name = os.path.splitext(filename)[0]
        extract_path = os.path.join(target_dir, plugin_name)

        print(f"📦 Bezig met: {filename}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Check op metadata.json
        meta_path = os.path.join(extract_path, "metadata.json")
        if not os.path.exists(meta_path):
            print(f"⚠️ Geen metadata.json gevonden in {plugin_name}, overslaan...")
            continue

        # Toon korte info uit metadata
        try:
            with open(meta_path) as f:
                meta = json.load(f)
            print(f"✅ Geïnstalleerd: {meta.get('name', plugin_name)} | versie: {meta.get('version', '1.0')}")
        except Exception as e:
            print(f"❌ Fout bij lezen van metadata in {plugin_name}: {e}")