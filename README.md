# build.lctimberframes.com — 3D model viewer

This repo is published as a static site at `build.lctimberframes.com`.

## Splash page (model picker)

- The site root (`/index.html`) is a splash page that reads `Models/manifest.json` and renders a list of models.
- Add your model files under `Models/` and add entries to `Models/manifest.json`.

## Supported model types

- **Cadwork-exported HTML**: add the exported `*.html` file under `Models/` and set `"type": "cadwork-html"` with `"href": "Models/your-file.html"`.
- **3D assets (optional)**: you can also host `*.glb`, `*.gltf`, `*.obj`, or `*.stl` under `Models/` and set `"type": "asset"` with `"src": "Models/your-file.glb"`. The splash page will open `viewer.html` for these.

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

