# 📤 Plugin upload

Follow these steps to share your plugin:

1. Create a folder containing:
   - `main.py` with your `PluginWidget` class
   - `metadata.json` with plugin details
   - `icon.png` (optional)
   - `preview.jpg` (optional screenshot)
2. Zip the folder, e.g. `myplugin.zip`.
3. Place the `.zip` in `/unofficial/` or `/official/` depending on your submission.
4. **Include `preview.jpg` inside the zip and list it in `metadata.json`:**
   ```json
   {
     "name": "MyPlugin",
     "preview": "preview.jpg"
   }
   ```
   The store reads this property to display your screenshot.
