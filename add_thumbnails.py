#!/usr/bin/env python3
"""
Script to automatically add thumbnail fields to manifest.json
for models that have Cover.webp files.
"""

import json
import os
from pathlib import Path

def add_thumbnails():
    # Load manifest
    with open('assets/manifest.json', 'r') as f:
        manifest = json.load(f)

    # Update each model
    for model in manifest['models']:
        if 'href' in model and model.get('type') == 'cadwork-html':
            # Extract directory from href
            href_parts = model['href'].split('/')
            if len(href_parts) >= 3:
                model_dir_name = href_parts[2]
                cover_path = f'assets/Models/{model_dir_name}/Cover.webp'

                # Check if Cover.webp exists
                if os.path.exists(cover_path):
                    # Add thumbnail field if it doesn't exist
                    if 'thumbnail' not in model:
                        model['thumbnail'] = cover_path
                        print(f"Added thumbnail to {model['name']}: {cover_path}")

    # Save updated manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print("Thumbnail update complete!")

if __name__ == '__main__':
    add_thumbnails()
