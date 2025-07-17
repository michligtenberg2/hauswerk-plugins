**🌐 Langues disponibles:** [Nederlands](../README.md) | [English](README_EN.md) | [Deutsch](README_DE.md) | [Français](README_FR.md) | [中文](README_ZH.md)

<link rel="stylesheet" href="theme.css">

# 🧹 Plugins Hauswerk (Français)

Bienvenue dans le dépôt **Hauswerk Plugins** — le dépôt officiel d’extensions pour l’interface graphique [Hauswerk](https://github.com/michligtenberg2/Hauswerk).

Ce dépôt contient des paquets `.zip` prêts à l’emploi, ainsi qu’un fichier central `plugins.json` utilisé par l’onglet **Plugin Store** dans l’application Hauswerk.

---

## 📦 Contenu du dépôt

| Plugin          | Description                                   | Fichier           |
|-----------------|------------------------------------------------|-------------------|
| Collage         | Crée un collage vidéo à partir de clips       | `collage.zip`     |
| Clipper         | Génère des extraits vidéo aléatoires          | `clipper.zip`     |
| Stretcher       | Ralentit des vidéos avec ou sans son          | `stretcher.zip`   |
| Concat          | Combine plusieurs vidéos                      | `concat.zip`      |
| Psychotisch     | Effet chaotique inspiré du style EBM          | `psychotisch.zip` |
| AudioFadeBPM    | Extraction audio par lot avec fondu BPM       | `audiofadebpm.zip`|
| UIBuilder       | Constructeur visuel de plugins                | `uibuilder.zip`   |

Chaque plugin comprend :
- un fichier `.py` avec une classe `QWidget`
- un fichier `plugin.json` contenant les métadonnées
- un fichier optionnel `.svg` (icône)
- *(optionnel)* `preview.png` (aperçu dans l’app)
- *(optionnel)* `tags` : ex. `["vidéo", "audio", "effet"]`

---

## 🔗 Index des plugins (`plugins.json`)

Le fichier [`plugins.json`](./plugins.json) suit ce format :

```json
{
  "name": "Collage",
  "description": "Plugin Collage pour Hauswerk.",
  "zip_url": "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/collage.zip",
  "tags": ["vidéo", "overlay"],
  "verified": true
}
```

Ce fichier est utilisé pour afficher, filtrer et installer les plugins dans Hauswerk.

---

## 🚧 Contribution et ajout de plugins

Deux façons d’ajouter un plugin :

```
╔════════════════════════════════════════════════════╗
║       📂 Répertoires de plugins et validation       ║
╠══════════════╦═════════════════════════════════════╣
║ /unofficial/ ║ Ouvert à tous (sans validation)      ║
║ /official/   ║ Requiert une pull request validée    ║
╚══════════════╩═════════════════════════════════════╝
```

### ✅ Option 1 : Libre via `/unofficial/`
- Ajouter votre `.zip` dans `/unofficial/`
- Le plugin sera automatiquement :
  - ✅ Validé (`plugin.json` requis)
  - ✅ Listé dans `unofficial/plugins.json`
  - ✅ Tagué et prévisualisé
- **Aucune approbation nécessaire**

### 🔐 Option 2 : Officiel via Pull Request
- Créez une pull request avec :
  - Votre plugin `.zip` dans `/official/`
  - Une entrée dans `plugins.json`
- Après validation, le plugin aura `verified: true`

| Méthode                   | Qui peut soumettre ? | Visible dans l’app ? | Revue requise ? |
|---------------------------|----------------------|------------------------|------------------|
| Upload dans `/unofficial/`| Tout le monde        | ✅ via store alternatif | ❌               |
| PR vers `/official/`      | Contributeurs        | ✅ dans l’onglet officiel| ✅              |

ℹ️ Le fichier `unofficial/plugins.json` est généré automatiquement à chaque push.

---

## 💡 Stores personnalisés

Hauswerk supporte plusieurs sources `plugins.json` :

```json
[
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/plugins.json",
  "https://votresite.fr/mystore/plugins.json",
  "https://github.com/michligtenberg2/hauswerk-plugins/raw/main/unofficial/plugins.json"
]
```

---

## 🛠️ Créer votre propre plugin

1. Créez un dossier contenant :
   - `monplugin.py`
   - `plugin.json`
   - *(optionnel)* `icon.svg`
   - *(optionnel)* `preview.png`

2. Zipper le dossier :
```bash
zip -r monplugin.zip monplugin/
```

3. Placer le `.zip` dans `/unofficial/`
4. C’est tout !
5. Pour un plugin officiel, ouvrez une pull request

---

## 🧹 Format du fichier `plugin.json`
```json
{
  "name": "MonPlugin",
  "entry": "monplugin.py",
  "class": "MonPluginWidget",
  "icon": "monplugin.svg",
  "tags": ["vidéo", "overlay"],
  "verified": false
}
```

---

## 🔄 Validation et mise à jour automatiques

Ce dépôt utilise [GitHub Actions](https://github.com/features/actions) pour :
- Valider le format de `plugins.json`
- Vérifier chaque `.zip` pour un `plugin.json`
- Générer `unofficial/plugins.json` automatiquement
- Ajouter tags, aperçu, champ `verified`
- (Optionnel) Actualiser des badges de store

---

## 📢 Contact & support
Des questions ou suggestions ? Ouvrez un ticket sur [github.com/michligtenberg2/Hauswerk](https://github.com/michligtenberg2/Hauswerk)

---

Bonne création à tous ! 🛠️
