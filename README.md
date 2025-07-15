# 🧹 Hauswerk Plugins
**🌐 Beschikbare talen:** [Nederlands](README.md) | [English](docs/README_EN.md) | [Deutsch](docs/README_DE.md) | [/Français](docs/README_FR.md) | [中文](docs/README_ZH.md)

![Plugin Count](https://img.shields.io/badge/plugins-7-blue)
![plugins.json](https://img.shields.io/badge/store-up--to--date-brightgreen)
![License](https://img.shields.io/github/license/michligtenberg2/Hauswerk-Plugins)

Welkom bij de **Hauswerk Plugins** repository — de officiële opslagplek voor uitbreidbare tools binnen de [Hauswerk](https://github.com/michligtenberg2/Hauswerk) GUI.

Deze repository bevat kant-en-klare plugins als `.zip` bestanden, samen met een centrale `plugins.json` die automatisch gebruikt wordt door de Plugin Store-tab binnen de Hauswerk-app.

---

## 📆 Wat zit er in deze repo?

| Plugin          | Beschrijving                             | Bestand        |
|-----------------|------------------------------------------|----------------|
| Collage         | Maakt een video-collage van clips        | `collage.zip`  |
| Clipper         | Genereert random clips uit een video     | `clipper.zip`  |
| Stretcher       | Vertraagt video's met of zonder audio    | `stretcher.zip`|
| Concat          | Voegt video's samen                      | `concat.zip`   |
| Psychotisch     | Creeër gekke EBM-style montage           | `psychotisch.zip` |
| AudioFadeBPM    | Batch audio extractie + crossfade        | `audiofadebpm.zip` |
| UIBuilder       | Visuele UI-pluginbouwer                  | `uibuilder.zip` |

Alle plugins bevatten minimaal:
- Één `.py` bestand met een `QWidget` subclass
- Een `plugin.json` bestand met metadata
- Een `.svg` icoon (optioneel)
- (optioneel) `preview.png` (wordt getoond in GUI)
- (optioneel) `tags`: lijst met trefwoorden zoals `"video"`, `"audio"`, `"glitch"`

---

## 🔗 Pluginlijst (plugins.json)

Het bestand [`plugins.json`](./plugins.json) bevat een lijst met alle beschikbare plugins in dit formaat:

```json
{
  "name": "Collage",
  "description": "Collage plugin voor Hauswerk.",
  "zip_url": "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/collage.zip",
  "tags": ["video", "overlay"],
  "verified": true
}
```

De Hauswerk-app gebruikt dit om plugins weer te geven, te filteren en te installeren via de ingebouwde Plugin Store.

---

## 🚧 Beheer & bijdragen

Er zijn twee manieren om plugins aan te leveren voor Hauswerk:

```
╔════════════════════════════════════════════════════╗
║           📂 Pluginstructuur en beoordeling         ║
╠══════════════╦═════════════════════════════════════╣
║ /unofficial/ ║ Open voor iedereen (geen keuring)   ║
║ /official/   ║ Alleen via pull request en review   ║
╚══════════════╩═════════════════════════════════════╝
```

### ✅ Methode 1: Open bijdrage via `/unofficial/`
- Voeg je `.zip` toe aan de map `/unofficial/`
- De plugin wordt automatisch:
  - ✅ gevalideerd (controle op geldige `plugin.json`)
  - ✅ toegevoegd aan `unofficial/plugins.json`
  - ✅ getagd, geteld en gepreviewd
- **Geen toestemming nodig**
- Handig voor experimenten of externe stores

### 🔐 Methode 2: Officiële opname via Pull Request
- Maak een pull request met:
  - Je `.zip` bestand in `/official/`
  - Toevoeging aan hoofd `plugins.json`
- De beheerder keurt dit handmatig goed
- Wordt dan onderdeel van de officiële store met `verified: true`

| Methode                      | Wie mag het? | Zichtbaar in app?         | Review nodig? |
|-----------------------------|--------------|----------------------------|----------------|
| Upload naar `/unofficial/` | Iedereen     | ✅ via unofficial store     | ❌             |
| PR naar `/official/`       | Contributors | ✅ via officiële plugin tab | ✅             |

ℹ️ `unofficial/plugins.json` wordt automatisch gegenereerd én geüpdatet bij elke wijziging in `/unofficial/`, inclusief tags en previews.

---

## 💡 Eigen stores en meerdere bronnen

Je bent vrij om je eigen plugin store te maken met een eigen `plugins.json`. De Hauswerk-app ondersteunt meerdere bronnen:

```json
[
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/plugins.json",
  "https://jouwdomein.nl/mijnstore/plugins.json",
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/unofficial/plugins.json"
]
```

Zo kunnen er officiële én experimentele stores tegelijk actief zijn in de interface.

---

## 🛠️ Een eigen plugin toevoegen

1. Maak een nieuwe submap met daarin:
   - `jouwplugin.py`
   - `plugin.json`
   - (optioneel) `icoon.svg`
   - (optioneel) `preview.png`

2. Zip de hele pluginmap:
```bash
zip -r jouwplugin.zip jouwplugin/
```

3. Voeg de `.zip` toe aan de map `/unofficial/`
4. Klaar! De plugin wordt automatisch zichtbaar in `unofficial/plugins.json`
5. Wil je officiële opname? Dien dan een PR in naar `/official/`

---

## 🧹 plugin.json format
Voorbeeld:
```json
{
  "name": "MijnPlugin",
  "entry": "mijnplugin.py",
  "class": "MijnPluginWidget",
  "icon": "mijnplugin.svg",
  "tags": ["video", "overlay"],
  "verified": false
}
```

---

## 🔄 Automatische validatie & pluginlijst

Deze repository gebruikt [GitHub Actions](https://github.com/features/actions) om:
- Te controleren of `plugins.json` geldig JSON is
- Elke `.zip` te controleren op aanwezigheid van `plugin.json`
- Een nieuwe `unofficial/plugins.json` te genereren **bij elke nieuwe plugin-upload**
- Automatisch tags, previews en plugin count bij te werken
- Mogelijkheid om dagelijks een `store badge` te refreshen

Zie `.github/workflows/validate_plugins.yml` voor de validatieregels.

---

## 📢 Ondersteuning / Contact
Voor vragen, bugs of ideeën: open een issue op [github.com/michligtenberg2/Hauswerk](https://github.com/michligtenberg2/Hauswerk).

---

Veel plezier met bouwen! 🛠️
