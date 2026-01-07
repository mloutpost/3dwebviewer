#!/usr/bin/env python3
"""
Script to update pricing in manifest.json from pricing.csv
"""

import json
import csv

def update_manifest_pricing():
    # Load manifest
    with open('assets/manifest.json', 'r') as f:
        manifest = json.load(f)

    # Load pricing data (handle commas in prices like sync_pricing.py does)
    pricing_data = {}
    with open('assets/pricing.csv', 'r') as f:
        lines = f.readlines()

    for line in lines[1:]:  # Skip header
        line = line.strip()
        if not line:
            continue

        # Split on first comma only (since prices may contain commas)
        first_comma_index = line.find(',')
        if first_comma_index == -1:
            continue

        model_id = line[:first_comma_index].strip()
        price = line[first_comma_index + 1:].strip()

        if model_id and price:
            pricing_data[model_id] = price

    # Update manifest with pricing
    updated_count = 0
    for model in manifest['models']:
        model_id = model['id']
        if model_id in pricing_data:
            model['price'] = pricing_data[model_id]
            updated_count += 1
            print(f"✅ Updated {model['name']}: {pricing_data[model_id]}")

    # Save updated manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n🎯 Successfully updated pricing for {updated_count} models!")

if __name__ == '__main__':
    update_manifest_pricing()