# build.lctimberframes.com — 3D model viewer

This repo is published as a static site at `build.lctimberframes.com`.

## Splash page (kit picker)

- The site root (`/index.html`) is a splash page that reads `Models/manifest.json` and renders a list of models.
- Add your model files under `Models/` and add entries to `Models/manifest.json`.

## Supported model types

- **Cadwork-exported HTML**: add the exported `*.html` file under `Models/` and set `"type": "cadwork-html"` with `"href": "Models/your-file.html"`.

## Example manifest entry

```json
{
  "id": "shed-frame",
  "name": "Shed Frame",
  "type": "cadwork-html",
  "href": "Models/shed-frame.html",
  "description": "Cadwork export"
}
```

