#!/usr/bin/env python3
"""
Script to URL-encode spaces in thumbnail paths in manifest.json
"""

import json
import urllib.parse

def fix_thumbnails():
    # Load manifest
    with open('assets/manifest.json', 'r') as f:
        manifest = json.load(f)

    # Update each model
    for model in manifest['models']:
        if 'thumbnail' in model:
            # URL encode the thumbnail path
            encoded_path = urllib.parse.quote(model['thumbnail'], safe='/:')
            if encoded_path != model['thumbnail']:
                print(f"Encoding: {model['thumbnail']} -> {encoded_path}")
                model['thumbnail'] = encoded_path

    # Save updated manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print("Thumbnail encoding complete!")

if __name__ == '__main__':
    fix_thumbnails()
