#!/usr/bin/env python3
"""
Script to add thumbnail fields to manifest.json for models with Cover.webp files
"""

import json
import os
from pathlib import Path

def add_thumbnails():
    # Load manifest
    with open('assets/manifest.json', 'r') as f:
        manifest = json.load(f)

    # Check each model for Cover.webp
    for model in manifest['models']:
        if model['type'] == 'cadwork-html':
            # Extract directory from href
            href_parts = model['href'].split('/')
            if len(href_parts) >= 3:
                model_dir_name = href_parts[2]
                cover_paths = [
                    f'assets/Models/{model_dir_name}/Cover.webp',
                    f'assets/Models/{model_dir_name}/cover.webp'
                ]

                for cover_path in cover_paths:
                    if os.path.exists(cover_path):
                        model['thumbnail'] = cover_path
                        print(f"✅ Added thumbnail to {model['name']}: {cover_path}")
                        break

    # Save updated manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print("Thumbnail addition complete!")

if __name__ == '__main__':
    add_thumbnails()