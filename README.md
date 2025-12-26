# build.lctimberframes.com — 3D model viewer

This repo is published as a static site at `build.lctimberframes.com`.

## Splash page (model picker)

- The site root (`/index.html`) is a splash page that reads `assets/manifest.json` and renders a list of models.
- Add your model files under `assets/` and add entries to `assets/manifest.json`.

## Supported model types

- **Cadwork-exported HTML**: create a folder per model under `assets/Models/` and put the exported `*.html` inside it:
  - Folder name: same as the HTML filename (without `.html`)
  - File path: `assets/Models/<model-name>/<model-name>.html`
  - Manifest: set `"type": "cadwork-html"` and `"href": "assets/Models/<model-name>/<model-name>.html"`
- **3D assets (optional)**: you can also host `*.glb`, `*.gltf`, `*.obj`, or `*.stl` under `assets/` and set `"type": "asset"` with `"src": "assets/your-file.glb"`. The splash page will open `viewer.html` for these.

## Cover images (home page thumbnails)

For each model folder under `assets/Models/<model-name>/`, you can add a cover image named `Cover` with one of these extensions:

- `Cover.webp`
- `Cover.png`
- `Cover.jpg`
- `Cover.jpeg`

If a model entry already has `"thumbnail"` in `assets/manifest.json`, that value will take precedence; otherwise the home page will automatically try to load a `Cover.*` image from the model’s folder.

## Example manifest entry

```json
{
  "id": "shed-frame",
  "name": "Shed Frame",
  "type": "cadwork-html",
  "href": "assets/Models/shed-frame/shed-frame.html",
  "description": "Cadwork export"
}
```

