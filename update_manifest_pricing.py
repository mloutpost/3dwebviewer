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

    # Load pricing data — CSV format: id,price,sale_price
    pricing_data = {}
    with open('assets/pricing.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) < 2 or not row[0].strip():
                continue
            model_id = row[0].strip()
            price = row[1].strip() if len(row) > 1 else ''
            sale_price = row[2].strip() if len(row) > 2 else ''
            if model_id and price:
                pricing_data[model_id] = (price, sale_price)

    # Update manifest with pricing and sale data
    updated_count = 0
    sale_count = 0
    for model in manifest['models']:
        model_id = model['id']
        if model_id in pricing_data:
            price, sale_price = pricing_data[model_id]
            if sale_price:
                model['price'] = sale_price
                model['originalPrice'] = price
                model['onSale'] = True
                sale_count += 1
                print(f"✅ Updated {model['name']}: {price} → SALE: {sale_price}")
            else:
                model['price'] = price
                model.pop('originalPrice', None)
                model.pop('onSale', None)
                print(f"✅ Updated {model['name']}: {price}")
            updated_count += 1

    # Save updated manifest
    with open('assets/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n🎯 Successfully updated pricing for {updated_count} models ({sale_count} on sale)!")

if __name__ == '__main__':
    update_manifest_pricing()