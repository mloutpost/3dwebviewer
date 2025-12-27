#!/usr/bin/env python3
"""
Script to automatically update gallery arrays in manifest.json
based on images found in renders directories.
"""

import json
import os
from pathlib import Path

def update_galleries():
    # Load manifest
    with open('assets/manifest.json', 'r') as f:
        manifest = json.load(f)
    
    # Supported image extensions
    image_exts = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
    
    # Update each model
    for model in manifest['models']:
        model_path = Path('assets/Models')
        model_dir = None
        
        # Find the model directory by matching href path
        if 'href' in model:
            href_parts = model['href'].split('/')
            if len(href_parts) >= 3:
                model_dir_name = href_parts[2]  # e.g., "LCTF Barn"
                potential_dir = model_path / model_dir_name
                if potential_dir.exists() and potential_dir.is_dir():
                    model_dir = potential_dir
        
        if model_dir:
            renders_dir = model_dir / 'renders'
            if renders_dir.exists():
                # Find all image files
                images = []
                for ext in image_exts:
                    images.extend(renders_dir.glob(f'*{ext}'))
                    images.extend(renders_dir.glob(f'*{ext.upper()}'))
                
                # Sort images by name for consistent ordering
                images.sort()
                
                # Create gallery URLs relative to the web root
                gallery_urls = []
                for img in images:
                    # Create URL path relative to web root
                    url_path = f'assets/Models/{model_dir_name}/renders/{img.name}'
                    gallery_urls.append(url_path)
                
                model['gallery'] = gallery_urls
                print(f"Updated {model['name']}: {len(gallery_urls)} images")
            else:
                model['gallery'] = []
    
    # Save updated manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("Gallery update complete!")

if __name__ == '__main__':
    update_galleries()
