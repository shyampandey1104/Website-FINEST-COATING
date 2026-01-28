#!/usr/bin/env python3
"""
Update HTML file - replace old Miscellaneous Cloudinary URLs with new Urinals URLs
"""

import shutil
from datetime import datetime

HTML_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"
BACKUP_FILE = f"/Users/shyamkumarpandey/html/blue_color_website_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

def main():
    print("=" * 80)
    print("🔄 UPDATE HTML - MISCELLANEOUS → URINALS")
    print("=" * 80)

    # Read HTML
    print(f"\n📖 Reading HTML file...")
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Create backup
    print(f"💾 Creating backup...")
    shutil.copy2(HTML_FILE, BACKUP_FILE)
    print(f"   Saved to: {BACKUP_FILE}")

    # Replace Miscellaneous with Urinals in URLs
    print("\n🔄 Replacing URLs...")

    old_pattern = "/Miscellaneous/"
    new_pattern = "/Urinals/"

    if old_pattern in html_content:
        count = html_content.count(old_pattern)
        html_content = html_content.replace(old_pattern, new_pattern)
        print(f"   ✅ Replaced {count} occurrences of '{old_pattern}' with '{new_pattern}'")

        # Save
        print(f"\n💾 Saving updated HTML...")
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ File updated successfully")
    else:
        print("   ⚠️  No Miscellaneous URLs found")

    print("\n✨ Done!\n")

if __name__ == "__main__":
    main()
