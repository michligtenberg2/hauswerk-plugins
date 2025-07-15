**🌐 Verfügbare Sprachen:** [Nederlands](../README.md) | [English](README_EN.md) | [Deutsch](README_DE.md) | [Français](README_FR.md) | [中文](README_ZH.md)

# 🧹 Hauswerk Plugins (Deutsch)

Willkommen im **Hauswerk Plugins**-Repository — der offiziellen Sammlung modularer Werkzeuge für die [Hauswerk](https://github.com/michligtenberg2/Hauswerk) GUI.

Dieses Repository enthält gebrauchsfertige Plugin-ZIPs sowie eine zentrale `plugins.json`, die den Plugin-Store in Hauswerk speist.

---

## 📦 Was ist in diesem Repository?

| Plugin          | Beschreibung                             | Datei          |
|-----------------|--------------------------------------------|----------------|
| Collage         | Erstellt eine Video-Collage mit Ebenen    | `collage.zip`  |
| Clipper         | Schneidet zufällige Clips aus einem Video | `clipper.zip`  |
| Stretcher       | Verlangsamt Videos (mit/ohne Audio)       | `stretcher.zip`|
| Concat          | Verbindet mehrere Videos zu einem         | `concat.zip`   |
| Psychotisch     | Chaotischer EBM-artiger Videoeffekt       | `psychotisch.zip` |
| AudioFadeBPM    | Audio extrahieren & crossfaden (Batch)    | `audiofadebpm.zip` |
| UIBuilder       | Visueller UI-Builder für Plugins          | `uibuilder.zip` |

Jedes Plugin enthält mindestens:
- Eine `.py`-Datei mit einer `QWidget`-Unterklasse
- Eine `plugin.json` mit Metadaten
- Optional ein `.svg`-Icon
- *(Optional)* `preview.png` (wird im Store angezeigt)
- *(Optional)* `tags`: z. B. `["video", "audio", "glitch"]`

---

## 🔗 Plugin-Liste (`plugins.json`)

Die Datei [`plugins.json`](./plugins.json) listet alle Plugins im folgenden Format:

```json
{
  "name": "Collage",
  "description": "Collage plugin for Hauswerk.",
  "zip_url": "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/collage.zip",
  "tags": ["video", "overlay"],
  "verified": true
}
```

Hauswerk verwendet diese Datei, um Plugins im Store anzuzeigen und zu filtern.

---

## 🚧 Beitrag & Plugin-Einreichung

Zwei Wege, ein Plugin beizutragen:

```
╔════════════════════════════════════════════════════╗
║      📂 Plugin-Verzeichnis & Freigabeprozess       ║
╠══════════════╦═════════════════════════════════════╣
║ /unofficial/ ║ Offen für alle (keine Freigabe)     ║
║ /official/   ║ Nur per Pull-Request & Prüfung       ║
╚══════════════╩═════════════════════════════════════╝
```

### ✅ Weg 1: Offen via `/unofficial/`
- Füge dein `.zip` in `/unofficial/` hinzu
- Das Plugin wird automatisch:
  - ✅ validiert (gültige `plugin.json` notwendig)
  - ✅ zu `unofficial/plugins.json` hinzugefügt
  - ✅ gezählt, mit Tags versehen und angezeigt
- **Keine Genehmigung nötig**

### 🔐 Weg 2: Offiziell via Pull Request
- Reiche einen PR ein mit:
  - deinem `.zip` in `/official/`
  - einem neuen Eintrag in `plugins.json`
- Nach Freigabe wird dein Plugin als `verified: true` gelistet

| Methode                 | Wer darf beitragen? | Sichtbar in App?           | Prüfung?        |
|------------------------|---------------------|-----------------------------|------------------|
| Upload in `/unofficial/` | Alle                | ✅ über inoffiziellen Store  | ❌               |
| PR in `/official/`       | Mitwirkende         | ✅ im offiziellen Store Tab  | ✅               |

ℹ️ `unofficial/plugins.json` wird automatisch generiert und aktualisiert bei jedem Push in `/unofficial/` — inkl. Tags & Previews.

---

## 💡 Eigene Stores & mehrere Quellen

Hauswerk unterstützt mehrere `plugins.json`-Quellen:

```json
[
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/plugins.json",
  "https://deinserver.de/meinstore/plugins.json",
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/unofficial/plugins.json"
]
```

So kannst du z. B. offizielle und eigene Plugins parallel laden.

---

## 🛠️ Eigenes Plugin erstellen

1. Erstelle einen Ordner mit:
   - `meinplugin.py`
   - `plugin.json`
   - *(optional)* `icon.svg`
   - *(optional)* `preview.png`

2. Zippen:
```bash
zip -r meinplugin.zip meinplugin/
```

3. `.zip` nach `/unofficial/` kopieren
4. Fertig! Das Plugin ist im inoffiziellen Store sichtbar
5. Willst du ins Offizielle? → PR an `/official/`

---

## 🧹 Format von `plugin.json`
Beispiel:
```json
{
  "name": "MeinPlugin",
  "entry": "meinplugin.py",
  "class": "MeinPluginWidget",
  "icon": "meinplugin.svg",
  "tags": ["video", "overlay"],
  "verified": false
}
```

---

## 🔄 Automatische Validierung & Generierung

Hauswerk verwendet [GitHub Actions](https://github.com/features/actions), um:
- `plugins.json` auf Syntax zu prüfen
- `.zip`-Dateien auf gültige `plugin.json` zu prüfen
- `unofficial/plugins.json` nach jedem Upload neu zu generieren
- Tags, Vorschauen und `verified` automatisch zu setzen
- Optional ein Store-Badge täglich zu aktualisieren

Siehe `.github/workflows/validate_plugins.yml` für Details.

---

## 📢 Kontakt & Support
Fragen oder Vorschläge? Öffne ein Issue auf [github.com/michligtenberg2/Hauswerk](https://github.com/michligtenberg2/Hauswerk).

---

Viel Spaß beim Entwickeln! 🛠️
