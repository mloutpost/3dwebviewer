# build.lctimberframes.com — 3D model viewer

This repo is published as a static site at `build.lctimberframes.com`.

## Splash page (model picker)

- The site root (`/index.html`) is a splash page that reads `assets/manifest.json` and renders a list of models.
- Add your model files under `assets/` and add entries to `assets/manifest.json`.

## Supported model types

- **Cadwork-exported HTML**: add the exported `*.html` file under `assets/Models/` and set `"type": "cadwork-html"` with `"href": "assets/Models/your-file.html"`.
- **3D assets (optional)**: you can also host `*.glb`, `*.gltf`, `*.obj`, or `*.stl` under `assets/` and set `"type": "asset"` with `"src": "assets/your-file.glb"`. The splash page will open `viewer.html` for these.

## Example manifest entry

```json
{
  "id": "shed-frame",
  "name": "Shed Frame",
  "type": "cadwork-html",
  "href": "assets/Models/shed-frame.html",
  "description": "Cadwork export"
}
```

