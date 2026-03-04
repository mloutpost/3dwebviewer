#!/usr/bin/env python3
"""Generate sitemap.xml from manifest.json. Run after manifest changes."""
import json
import os

BASE = "https://shoptimberframekits.com"
MANIFEST = "assets/manifest.json"
OUT = "sitemap.xml"

def main():
    with open(MANIFEST) as f:
        data = json.load(f)
    models = [m for m in data.get("models", []) if not m.get("hidden")]

    urls = [
        ("/", "weekly", "1.0"),
        ("/inquiry.html", "monthly", "0.9"),
        ("/claim-kit.html", "monthly", "0.9"),
        ("/custom-design.html", "monthly", "0.9"),
        ("/privacy.html", "yearly", "0.3"),
        ("/eula.html", "yearly", "0.3"),
    ]
    for m in models:
        urls.append((f"/detail.html?id={m['id']}", "monthly", "0.8"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, freq, pri in urls:
        lines.append(f"  <url>")
        lines.append(f"    <loc>{BASE}{path}</loc>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        lines.append(f"  </url>")
    lines.append("</urlset>")

    with open(OUT, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {OUT} with {len(urls)} URLs ({len(models)} product pages)")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    main()
