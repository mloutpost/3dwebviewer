#!/usr/bin/env python3
"""
Script to reindex all models from the Models directory and update manifest.json
"""

import json
import os
from pathlib import Path

def get_model_type(model_dir):
    """Determine model type based on directory contents"""
    html_files = list(model_dir.glob("*.html"))
    if html_files:
        return "cadwork-html"
    else:
        return "coming-soon"

def get_model_href(model_dir, model_type):
    """Get the href for cadwork-html models"""
    if model_type != "cadwork-html":
        return ""

    html_files = list(model_dir.glob("*.html"))
    if html_files:
        return f"assets/Models/{model_dir.name}/{html_files[0].name}"
    return ""

def get_model_name(model_dir):
    """Extract model name from directory name with some cleaning"""
    name = model_dir.name

    # Handle new SN-prefixed directory names (e.g., "LC_101 - 48x60 Equestrian Barn")
    if " - " in name:
        # Extract the part after " - "
        sn_part, model_part = name.split(" - ", 1)
        name = model_part.strip()

    # Handle specific known mappings for the cleaned names
    name_mappings = {
        "36x42 Monitor Barn Web Viewer": "36x42 Monitor Barn",
        "33x39 LCTF Barn": "LCTF Barn",
        "48x60 Equestrian Barn": "48x60 Equestrian Barn",
        "36x52 Dairy Barn": "36x52 Dairy Barn",
        "21x24 Old Natchez Studio": "24x21 Studio Shed",
        "22x66 Old Natchez Trace (Full Size)": "Old Natchez Trace",
        "38x44 Monitor Barn": "38x44 Monitor Barn",
        "24x30 Cottage": "24x30 Cottage",
        "Bee Tree Hill": "Bee Tree Hill Barn",
        "50' Covered Bridge": "50' Covered Bridge",
        "Old Natchez Decorative Element": "Old Natchez Decorative Element",
        "Old Natchez Reduced": "Old Natchez Reduced",
        "Hammer Beam Pavilion 14x18 V1.1.1": "14x18 Hammer Beam Pavilion",
        "Simple Curve Pavilion 10x16 V1.1.1": "10x16 Simple Curve Pavilion",
        "Cruck Pavilion 14x20 V1.2.1": "14x20 Cruck Pavilion",
        "Scissor Truss Pavilion 16x18 V1.2.1": "16x18 Scissor Truss Pavilion",
        "Simple Corbel": "Simple Corbel",
        "One Piece Corbel": "Standalone Corbel",
        "Angled Corbel": "Angled Corbel",
        "Simple Entryway": "Simple Entryway",
        "Scissor Truss Entryway": "Scissor Entryway",
        "Curved Truss Entryway": "Curved Truss Entryway",
        "Simple Pergola 12x16": "12x16 Simple Pergola",
        "Simple Pergola 12x18 V1.1.1": "12x18 Pergola",
        "Slanted Pergola 12x16 V1.1.1": "12x16 Pergola",
        "Simple Pergola 10x16 V1.1.1": "10x16 Simple Pergola",
        "Simple Pavilion 16x24 3.1.1": "16x24 King Post Pavilion",
        "Simple Pergola 14x22 V1.1.1": "14x22 Pergola",
        "Simple 14x22 Modified": "14x22 Modified Pergola"
    }

    return name_mappings.get(name, name)

def get_model_id(model_dir):
    """Generate model ID from directory name using SN codes"""
    name = model_dir.name

    # Extract SN code from directory name (e.g., "LC_101 - 48x60 Equestrian Barn" -> "LC_101")
    if " - " in name:
        sn_code = name.split(" - ")[0].strip()
    else:
        sn_code = name

    # Handle specific ID mappings based on SN codes
    id_mappings = {
        "LC_101": "lone-oak-barn",
        "LC_102": "notch-barn",
        "LC_103": "24x30-cottage",
        "LC_104": "50-covered-bridge",
        "LC_105": "bee-tree-hill",
        "LC_106": "20x36-cruck-pavilion",
        "LC_107": "36x42-monitor-barn",
        "LC14": "38x44-monitor-barn",
        "LC19": "old-natchez-trace",
        "LC19_1": "lc19-1-old-natchez-decorative-element",
        "LC19_R": "lc19-old-natchez-reduced",
        "LC20": "lctf-barn",
        "LC22": "old-natchez-studio",
        "LCTF PF1": "lctf-pf1",
        "LCTF PF2": "lctf-pf2",
        "LCTF PF3": "lctf-pf3",
        "LCTF PF4": "lctf-pf4",
        "LCTF PF5": "lctf-pf5",
        "LCTF PF6": "lctf-pf6",
        "LCTF PF7": "lctf-pf7",
        "LCTF PF8": "lctf-pf8",
        "LCTF PF9": "lctf-pf9",
        "LCTF PF10": "lctf-pf10",
        "LCTF PF11": "lctf-pf11",
        "LCTF PF12": "lctf-pf12",
        "LCTF PF13": "lctf-pf13",
        "LCTF PF14": "lctf-pf14",
        "LCTF PF15": "lctf-pf15",
        "LCTF PF16": "lctf-pf16",
        "LCTF PF17": "lctf-pf17",
        "LCTF PF18": "lctf-pf18",
        "LCTF PF19": "lctf-pf19"
    }

    return id_mappings.get(sn_code, sn_code.lower().replace(' ', '-').replace('_', '-'))

def get_model_tag(model_name):
    """Determine model tag/category"""
    name_lower = model_name.lower()

    if 'barn' in name_lower:
        return 'Barns'
    elif 'pavilion' in name_lower or 'pergola' in name_lower:
        return 'Pavilion/Pergola'
    elif 'entry' in name_lower or 'entryway' in name_lower:
        return 'Entries'
    elif 'corbel' in name_lower:
        return 'Decorative'
    else:
        return 'Other'

def reindex_models():
    models_dir = Path("assets/Models")
    models = []

    print("🔍 Scanning Models directory...")

    # Get all subdirectories
    model_dirs = sorted([d for d in models_dir.iterdir() if d.is_dir()])

    for model_dir in model_dirs:
        if model_dir.name.startswith('.'):
            continue  # Skip hidden directories

        model_type = get_model_type(model_dir)
        model_name = get_model_name(model_dir)
        model_id = get_model_id(model_dir)
        model_tag = get_model_tag(model_name)

        model = {
            "id": model_id,
            "name": model_name,
            "type": model_type,
            "href": get_model_href(model_dir, model_type),
            "description": f"{model_name} with timber frame construction",
            "tag": model_tag,
            "price": "coming soon",
            "features": [
                f"{model_name.split()[0]} footprint",
                "Timber frame construction"
            ],
            "gallery": []
        }

        # Add thumbnail if Cover.webp exists
        cover_path = model_dir / "Cover.webp"
        if cover_path.exists():
            model["thumbnail"] = f"assets/Models/{model_dir.name}/Cover.webp"

        # Add gallery images if they exist
        renders_dir = model_dir / "renders"
        if renders_dir.exists():
            gallery_files = sorted([f for f in renders_dir.glob("*.webp") if not f.name.startswith('.')])
            model["gallery"] = [f"assets/Models/{model_dir.name}/renders/{f.name}" for f in gallery_files]

        models.append(model)
        print(f"✅ Indexed: {model_name} ({model_type})")

    # Create manifest
    manifest = {
        "models": models
    }

    # Save manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n🎯 Successfully reindexed {len(models)} models!")
    print(f"📊 {sum(1 for m in models if m['type'] == 'cadwork-html')} HTML models")
    print(f"📋 {sum(1 for m in models if m['type'] == 'coming-soon')} coming-soon models")

if __name__ == '__main__':
    reindex_models()
