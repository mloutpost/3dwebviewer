#!/usr/bin/env python3
"""
Script to decode URL-encoded thumbnail paths in manifest.json
"""

import json
import urllib.parse

def unencode_thumbnails():
    # Load manifest
    with open('assets/manifest.json', 'r') as f:
        manifest = json.load(f)

    # Update each model
    for model in manifest['models']:
        if 'thumbnail' in model:
            # URL decode the thumbnail path
            decoded_path = urllib.parse.unquote(model['thumbnail'])
            if decoded_path != model['thumbnail']:
                print(f"Decoding: {model['thumbnail']} -> {decoded_path}")
                model['thumbnail'] = decoded_path

    # Save updated manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print("Thumbnail decoding complete!")

if __name__ == '__main__':
    unencode_thumbnails()
