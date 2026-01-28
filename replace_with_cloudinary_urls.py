#!/usr/bin/env python3
"""
Replace local image paths in HTML with Cloudinary URLs
"""

import json
import re
import shutil
from datetime import datetime

# Paths
HTML_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"
RESULTS_FILE = "/Users/shyamkumarpandey/html/cloudinary_upload_results.json"
BACKUP_FILE = f"/Users/shyamkumarpandey/html/blue_color_website_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

def main():
    print("=" * 80)
    print("🔄 REPLACE LOCAL IMAGES WITH CLOUDINARY URLS")
    print("=" * 80)

    # Load upload results
    print(f"\n📖 Loading upload results from: {RESULTS_FILE}")
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        results = json.load(f)

    uploaded = results['uploaded']
    print(f"✅ Found {len(uploaded)} uploaded images")

    # Create backup
    print(f"\n💾 Creating backup: {BACKUP_FILE}")
    shutil.copy2(HTML_FILE, BACKUP_FILE)
    print("✅ Backup created")

    # Read HTML
    print(f"\n📖 Reading HTML file: {HTML_FILE}")
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Replace each local path with Cloudinary URL
    print("\n🔄 Replacing image paths...")
    replacements_made = 0

    for item in uploaded:
        local_path = item['local_path']
        cloudinary_url = item['cloudinary_url']

        # Find all occurrences of the local path in src attributes
        # Pattern: src="local_path" or src='local_path'
        patterns = [
            f'src="{local_path}"',
            f"src='{local_path}'"
        ]

        for pattern in patterns:
            if pattern in html_content:
                # Determine which quote style to use
                quote = '"' if '"' in pattern else "'"
                replacement = f'src={quote}{cloudinary_url}{quote}'

                html_content = html_content.replace(pattern, replacement)
                replacements_made += 1
                print(f"   ✅ {local_path} → Cloudinary URL")

    # Save updated HTML
    if replacements_made > 0:
        print(f"\n💾 Saving updated HTML...")
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Saved with {replacements_made} replacements")
    else:
        print("\n⚠️  No replacements made")

    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"Total images uploaded: {len(uploaded)}")
    print(f"Replacements made: {replacements_made}")
    print(f"Backup file: {BACKUP_FILE}")
    print(f"Updated file: {HTML_FILE}")
    print("=" * 80)
    print("\n✨ Done!\n")

if __name__ == "__main__":
    main()
