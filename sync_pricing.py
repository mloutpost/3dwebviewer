#!/usr/bin/env python3
"""
Script to sync pricing from Google Sheets to local CSV
Usage: python3 sync_pricing.py
"""

import csv
import urllib.request
import urllib.parse
import ssl

# Google Sheets CSV export URL
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1763KWbOgtVHSFSDvOUW0NnXTIF3nyvZHqFDrN_BoQHw/export?format=csv&gid=0"

# SN to ID mappings
SN_MAPPING = {
    'LC14': 'lc14-monitor-barn',
    'LCTF_PF1': 'lctf-pf1',
    'LCTF_PF2': 'lctf-pf2',
    'LCTF_PF3': 'lctf-pf3',
    'LCTF_PF4': 'lctf-pf4',
    'LCTF_PF9': 'lctf-pf9',
    'LCTF_PF10': 'lctf-pf10',
    'LCTF_PF11': 'lctf-pf11',
    'LCTF_PF12': 'lctf-pf12',
    'LCTF_PF13': 'lctf-pf13',
    'LCTF_PF14': 'lctf-pf14',
    'LCTF_PF15': 'lctf-pf15',
    'LCTF_PF16': 'lctf-pf16',
    'LCTF_PF17': 'lctf-pf17',
    'LCTF_PF18': 'lctf-pf18',
    'LC_101': 'lone-oak-barn',
    'LC_102': 'notch-barn',
    'LC20': 'lctf-barn',
    'LC22': 'old-natchez-studio',
    'LC_103': '38x44-monitor-barn',  # Assuming this is the monitor barn
    'LC_105': 'bee-tree-hill',  # Assuming this is bee tree hill barn
    'LCTF_PF19': 'lctf-pf19',
    'LC_19': 'old-natchez-trace',
    'LC_107': '24x30-cottage'  # Assuming this is the cottage
}

def format_price(price_str):
    """Format price with dollar sign and commas"""
    try:
        num = int(price_str.replace(',', ''))
        return f"${num:,}"
    except:
        return price_str

def sync_pricing():
    print("🔄 Syncing pricing from Google Sheets...")

    try:
        # Fetch CSV from Google Sheets (bypass SSL for compatibility)
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(GOOGLE_SHEETS_URL, context=context) as response:
            csv_content = response.read().decode('utf-8')

        # Parse CSV
        lines = csv_content.split('\n')
        reader = csv.reader(lines)
        rows = list(reader)

        if len(rows) < 2:
            print("❌ No data found in Google Sheet")
            return

        pricing_data = {}

        # Skip header row
        for row in rows[1:]:
            if len(row) >= 5:
                sn = row[0].strip()
                price = row[4].strip()

                # Only process rows with valid SN and price
                if sn and price and price not in ['Yes', 'No', ''] and price.isdigit():
                    # Map SN to model ID
                    model_id = SN_MAPPING.get(sn)
                    if model_id:
                        formatted_price = format_price(price)
                        pricing_data[model_id] = formatted_price
                        print(f"✅ {sn} → {model_id}: {formatted_price}")
                    else:
                        print(f"⚠️  {sn} not in mapping - skipping")

        if not pricing_data:
            print("❌ No valid pricing data found")
            return

        # Write to local CSV (no quotes)
        with open('assets/pricing.csv', 'w') as csvfile:
            csvfile.write('id,price\n')
            for model_id, price in pricing_data.items():
                csvfile.write(f'{model_id},{price}\n')

        print(f"🎯 Successfully synced {len(pricing_data)} pricing entries to assets/pricing.csv")
        print("💡 Refresh your website to see updated pricing!")

    except Exception as e:
        print(f"❌ Error syncing pricing: {e}")

if __name__ == '__main__':
    sync_pricing()
