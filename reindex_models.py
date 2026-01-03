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

    # Handle specific known mappings
    name_mappings = {
        "LC14 36x42 Monitor Barn Web Viewer": "36x42 Monitor Barn",
        "33x39 LCTF Barn": "LCTF Barn",
        "48x60 Equestrian Barn": "48x60 Equestrian Barn",
        "36x52 Dairy Barn": "36x52 Dairy Barn",
        "21x24 Old Natchez Studio": "24x21 Studio Shed",
        "22x66 Old Natchez Trace (Full Size)": "Old Natchez Trace",
        "LCTF PF1 Hammer Beam Pavilion 14x18 V1.1.1": "14x18 Hammer Beam Pavilion",
        "LCTF PF2 Simple Curve Pavilion 10x16 V1.1.1": "10x16 Simple Curve Pavilion",
        "LCTF PF3 Cruck Pavilion 14x20 V1.2.1": "14x20 Cruck Pavilion",
        "LCTF PF4 Scissor Truss Pavilion 16x18 V1.2.1": "16x18 Scissor Truss Pavilion",
        "LCTF PF5 Simple Corbel": "Simple Corbel",
        "LCTF PF6 Simple Corbel": "Simple Corbel",
        "LCTF PF7 One Piece Corbel": "Standalone Corbel",
        "LCTF PF8 Angled Corbel": "Angled Corbel",
        "LCTF PF9 Simple Entryway": "Simple Entryway",
        "LCTF PF10 Scissor Truss Entryway": "Scissor Entryway",
        "LCTF PF11 Curved Truss Entryway": "Curved Truss Entryway",
        "LCTF PF12 Simple Entryway": "Simple Entryway",
        "LCTF PF13 Simple Pergola 12x16": "12x16 Simple Pergola",
        "LCTF PF14 Simple Pergola 12x18 V1.1.1": "12x18 Pergola",
        "LCTF PF15 Slanted Pergola 12x16 V1.1.1": "12x16 Pergola",
        "LCTF PF16 Simple Pergola 10x16 V1.1.1": "10x16 Simple Pergola",
        "LCTF PF17 Simple Pavilion 16x24 3.1.1": "16x24 King Post Pavilion",
        "LCTF PF18 Simple Pergola 14x22 V1.1.1": "14x22 Pergola",
        "LCTF PF19 Simple 14x22 Modified": "14x22 Modified Pergola"
    }

    return name_mappings.get(name, name)

def get_model_id(model_dir):
    """Generate model ID from directory name"""
    name = model_dir.name.lower()

    # Handle specific ID mappings
    id_mappings = {
        "lc14 36x42 monitor barn web viewer": "lc14-monitor-barn",
        "33x39 lctf barn": "lctf-barn",
        "48x60 equestrian barn": "lone-oak-barn",
        "36x52 dairy barn": "notch-barn",
        "21x24 old natchez studio": "old-natchez-studio",
        "22x66 old natchez trace (full size)": "old-natchez-trace",
        "lctf pf1 hammer beam pavilion 14x18 v1.1.1": "lctf-pf1",
        "lctf pf2 simple curve pavilion 10x16 v1.1.1": "lctf-pf2",
        "lctf pf3 cruck pavilion 14x20 v1.2.1": "lctf-pf3",
        "lctf pf4 scissor truss pavilion 16x18 v1.2.1": "lctf-pf4",
        "lctf pf5 simple corbel": "lctf-pf5",
        "lctf pf6 simple corbel": "lctf-pf6",
        "lctf pf7 one piece corbel": "lctf-pf7",
        "lctf pf8 angled corbel": "lctf-pf8",
        "lctf pf9 simple entryway": "lctf-pf9",
        "lctf pf10 scissor truss entryway": "lctf-pf10",
        "lctf pf11 curved truss entryway": "lctf-pf11",
        "lctf pf12 simple entryway": "lctf-pf12",
        "lctf pf13 simple pergola 12x16": "lctf-pf13",
        "lctf pf14 simple pergola 12x18 v1.1.1": "lctf-pf14",
        "lctf pf15 slanted pergola 12x16 v1.1.1": "lctf-pf15",
        "lctf pf16 simple pergola 10x16 v1.1.1": "lctf-pf16",
        "lctf pf17 simple pavilion 16x24 3.1.1": "lctf-pf17",
        "lctf pf18 simple pergola 14x22 v1.1.1": "lctf-pf18",
        "lctf pf19 simple 14x22 modified": "lctf-pf19"
    }

    # Convert to ID format
    id = name.replace(' ', '-').replace('_', '-')
    return id_mappings.get(name, id)

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
