**🌐 Available Languages:** [../Nederlands](README.md) | [English](README_EN.md) | [Deutsch](README_DE.md) | [Français](README_FR.md) | [中文](README_ZH.md)

# 🧹 Hauswerk Plugins

![Plugin Count](https://img.shields.io/badge/plugins-7-blue)
![plugins.json](https://img.shields.io/badge/store-up--to--date-brightgreen)
![License](https://img.shields.io/github/license/michligtenberg2/Hauswerk_Plugins)

Welcome to the **Hauswerk Plugins** repository — the official collection of modular tools for the [Hauswerk](https://github.com/michligtenberg2/Hauswerk) GUI.

This repository contains ready-to-use `.zip` plugin packages and a central `plugins.json` file that powers the Plugin Store tab inside the Hauswerk application.

---

## 📆 What's in this repo?

| Plugin          | Description                             | File           |
|-----------------|------------------------------------------|----------------|
| Collage         | Create a layered video collage           | `collage.zip`  |
| Clipper         | Generate random clips from a video       | `clipper.zip`  |
| Stretcher       | Slow down videos (with or without audio) | `stretcher.zip`|
| Concat          | Concatenate videos into one file         | `concat.zip`   |
| Psychotisch     | Chaotic EBM-style editing effect         | `psychotisch.zip` |
| AudioFadeBPM    | Batch extract + crossfade audio          | `audiofadebpm.zip` |
| UIBuilder       | Visual plugin UI builder                 | `uibuilder.zip` |

Each plugin includes at minimum:
- One `.py` file containing a `QWidget` subclass
- A `plugin.json` with metadata
- An optional `.svg` icon
- *(Optional)* `preview.png` (shown in the Plugin Store)
- *(Optional)* `tags` field like `["video", "audio", "glitch"]`

---

## 🔗 Plugin index (`plugins.json`)

The [`plugins.json`](./plugins.json) file lists all available plugins in this format:

```json
{
  "name": "Collage",
  "description": "Collage plugin for Hauswerk.",
  "zip_url": "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/collage.zip",
  "tags": ["video", "overlay"],
  "verified": true
}
```

The Hauswerk app uses this to display, filter and install plugins from the Plugin Store tab.

---

## 🚧 Contributing & Plugin Submission

There are two ways to submit plugins to Hauswerk:

```
╔════════════════════════════════════════════════════╗
║         📂 Plugin Directory & Approval Flow        ║
╠══════════════╦═════════════════════════════════════╣
║ /unofficial/ ║ Open for everyone (no review)       ║
║ /official/   ║ Via pull request + manual approval  ║
╚══════════════╩═════════════════════════════════════╝
```

### ✅ Option 1: Open Submission via `/unofficial/`
- Add your `.zip` file to the `/unofficial/` folder
- The plugin will automatically:
  - ✅ be validated (must contain valid `plugin.json`)
  - ✅ be added to `unofficial/plugins.json`
  - ✅ be counted, tagged, and previewed
- **No permission or pull request needed**
- Great for testing or external sharing

### 🔐 Option 2: Official Submission via Pull Request
- Open a pull request that includes:
  - Your `.zip` file in `/official/`
  - A new entry in the main `plugins.json`
- A maintainer will manually approve the plugin
- Once merged, the plugin will be `verified: true`

| Method                      | Who can submit? | Visible in app?           | Review required? |
|----------------------------|------------------|----------------------------|-------------------|
| Upload to `/unofficial/`   | Anyone           | ✅ via unofficial store     | ❌                |
| PR to `/official/`         | Contributors     | ✅ via official store tab   | ✅                |

ℹ️ The `unofficial/plugins.json` is automatically generated and updated on each push to `/unofficial/` — including tags and previews.

---

## 💡 Custom stores and multiple sources

You can host your own plugin store with a `plugins.json`. The Hauswerk app supports loading from multiple sources:

```json
[
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/plugins.json",
  "https://yourdomain.com/customstore/plugins.json",
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/unofficial/plugins.json"
]
```

This allows official and experimental plugins to be shown side by side.

---

## 🛠️ How to create your own plugin

1. Create a folder with:
   - `yourplugin.py`
   - `plugin.json`
   - *(optional)* `icon.svg`
   - *(optional)* `preview.png`

2. Zip the entire plugin:
```bash
zip -r yourplugin.zip yourplugin/
```

3. Add the `.zip` to `/unofficial/`
4. Done! It will appear in the app under unofficial plugins
5. Want to go official? Open a PR to `/official/`

---

## 🧹 `plugin.json` format
Example:
```json
{
  "name": "MyPlugin",
  "entry": "myplugin.py",
  "class": "MyPluginWidget",
  "icon": "myplugin.svg",
  "tags": ["video", "overlay"],
  "verified": false
}
```

---

## 🔄 Auto-validation & store generation

This repo uses [GitHub Actions](https://github.com/features/actions) to:
- Validate `plugins.json` formatting
- Check that each `.zip` includes a valid `plugin.json`
- Regenerate `unofficial/plugins.json` on every plugin upload
- Automatically populate tags, previews and verification fields
- Optionally refresh plugin store badge daily

See `.github/workflows/validate_plugins.yml` for details.

---

## 📢 Support & Contact
For questions, bugs or suggestions: open an issue at [github.com/michligtenberg2/Hauswerk](https://github.com/michligtenberg2/Hauswerk).

---

Happy building! 🛠️
