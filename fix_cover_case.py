#!/usr/bin/env python3
"""
Script to fix case sensitivity issues in cover image paths in manifest.json
"""

import json
import os
from pathlib import Path

def fix_cover_case():
    # Load manifest
    with open('assets/manifest.json', 'r') as f:
        manifest = json.load(f)

    # Check each model with thumbnail
    for model in manifest['models']:
        if 'thumbnail' in model:
            thumbnail_path = model['thumbnail']

            # Check if the path exists as-is
            if not os.path.exists(thumbnail_path):
                # Try different case variations
                dir_path = os.path.dirname(thumbnail_path)
                filename = os.path.basename(thumbnail_path)

                # Try lowercase
                lowercase_path = os.path.join(dir_path, filename.lower())
                if os.path.exists(lowercase_path):
                    model['thumbnail'] = lowercase_path
                    print(f"Fixed case: {thumbnail_path} -> {lowercase_path}")
                    continue

                # Try uppercase
                uppercase_path = os.path.join(dir_path, filename.upper())
                if os.path.exists(uppercase_path):
                    model['thumbnail'] = uppercase_path
                    print(f"Fixed case: {thumbnail_path} -> {uppercase_path}")
                    continue

                print(f"Warning: Cover file not found: {thumbnail_path}")

    # Save updated manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print("Cover case fixing complete!")

if __name__ == '__main__':
    fix_cover_case()
