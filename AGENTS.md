# AGENT instructions for hauswerk-plugins

This repository hosts modular plugin packages for the Hauswerk application. The documentation in `README.md` and the files under `docs/` describe how plugins are packaged, validated and distributed.

## Repository highlights
- Plugins are bundled as `.zip` archives containing a Python `QWidget` implementation, a `plugin.json` metadata file and optional resources (icon, preview image).
- Official plugins live in `official/` and community uploads go into `unofficial/`.
- The root `plugins.json` provides an index of available plugins for the Hauswerk store.
- GitHub Actions validate plugin archives and regenerate `unofficial/plugins.json` automatically.

## Development guidelines
- **Modularity**: design plugins so that each is self-contained and communicates with Hauswerk only through the expected metadata and widget class.
- Ensure `plugins.json` is valid JSON after changes by running `python -m json.tool plugins.json`.
- When adding or updating plugins, follow the folder structure explained in the documentation: include a `.py` file, `plugin.json`, and optionally an `.svg` icon and preview.

## Binary files
Binary uploads are disabled in this environment. Avoid committing files such as `.jpg`, `.png`, `.zip`, or other binary formats. If you need to include an image, encode it to base64 and store it in a text file.

