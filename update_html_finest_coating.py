#!/usr/bin/env python3
"""
Update HTML file with Finest Coating Cloudinary URLs
"""

import re
import json

# Files
HTML_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"
JSON_FILE = "/Users/shyamkumarpandey/html/finest_coating_urls.json"

# Load URLs
with open(JSON_FILE, 'r') as f:
    urls = json.load(f)

# Read HTML
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

original_html = html

print("=" * 60)
print("🔄 Updating HTML with Finest Coating URLs")
print("=" * 60)

# Create organized URL mappings
HERO = urls.get("hero/hero-bathtub.png") or urls.get("hero/hero_bathtub.png")

BATHTUB_BEFORE = [
    urls.get("bathtub/before/bathtub-before1.jpg"),
    urls.get("bathtub/before/bathtub-before2.jpg"),
    urls.get("bathtub/before/bathtub-before3.jpg"),
    urls.get("bathtub/before/bathtub-before4.jpg"),
    urls.get("bathtub/before/bathtub-before5.jpg"),
    urls.get("bathtub/before/bathtub-before6.jpg"),
]

BATHTUB_AFTER = [
    urls.get("bathtub/after/bathtub-after1.jpg"),
    urls.get("bathtub/after/bathtub-after2.jpg"),
    urls.get("bathtub/after/bathtub-after3.jpg"),
    urls.get("bathtub/after/bathtub-after4.jpg"),
    urls.get("bathtub/after/bathtub-after5.jpg"),
    urls.get("bathtub/after/bathtub-after6.jpg"),
]

BATHTUB_GALLERY = urls.get("bathtub/bathtub-refinishing.png")

BATHROOM = [v for k, v in urls.items() if k.startswith("bathroom/")]

URINALS = [
    urls.get("urinals/How-To-Keep-Urinals-Clean.jpg"),
    urls.get("urinals/download.jpeg"),
    urls.get("urinals/download1.jpeg"),
    urls.get("urinals/download2.jpeg"),
    urls.get("urinals/download3.jpeg"),
    urls.get("urinals/images.jpeg"),
]

KITCHEN = [
    urls.get("kitchen/kitchen1.jpeg"),
    urls.get("kitchen/kitchen2.jpeg"),
    urls.get("kitchen/kitchen3.jpeg"),
    urls.get("kitchen/kitchen4.jpg"),
    urls.get("kitchen/kitchen5.jpeg"),
    urls.get("kitchen_folder/Gemini_Generated_Image_xw8bg5xw8bg5xw8b.png"),
    urls.get("kitchen_folder/Gemini_Generated_Image_ggp5esggp5esggp5.png"),
]

BUFFING = [
    urls.get("buffing/buffing1.jpeg"),
    urls.get("buffing/buffing2.jpeg"),
    urls.get("buffing/buffing3.jpeg"),
]

DECORATIVE = urls.get("decorative/decorative-items.jpeg")

INDUSTRIAL = [v for k, v in urls.items() if k.startswith("industrial/")]

SERVICES = [v for k, v in urls.items() if k.startswith("services/")]

OTHER = [
    urls.get("other/benefits-image-2.jpeg"),
    urls.get("other/faq-image-2.jpeg"),
]

# Filter None values
BATHTUB_BEFORE = [u for u in BATHTUB_BEFORE if u]
BATHTUB_AFTER = [u for u in BATHTUB_AFTER if u]
BATHROOM = [u for u in BATHROOM if u]
URINALS = [u for u in URINALS if u]
KITCHEN = [u for u in KITCHEN if u]
BUFFING = [u for u in BUFFING if u]
INDUSTRIAL = [u for u in INDUSTRIAL if u]
SERVICES = [u for u in SERVICES if u]
OTHER = [u for u in OTHER if u]

replacements = 0

# Replace any existing Cloudinary URLs or old URLs
print("\n📷 Replacing image URLs...")

# 1. Replace all Unsplash URLs
unsplash_pattern = r'https://images\.unsplash\.com/[^"\']+'
def replace_unsplash(match):
    global replacements
    replacements += 1
    return BATHROOM[replacements % len(BATHROOM)] if BATHROOM else match.group(0)

html = re.sub(unsplash_pattern, replace_unsplash, html)
print(f"   ✅ Unsplash URLs replaced")

# 2. Replace old Cloudinary URLs (any pattern)
old_cloudinary_pattern = r'https://res\.cloudinary\.com/dd2sbrcrr/image/upload/[^"\']+/(?:Abdul%20Images|Shyam|Finest_Coating)[^"\']+'

counter = {'val': 0}
def replace_old_cloudinary(match):
    counter['val'] += 1
    url = match.group(0).lower()

    if 'urinal' in url:
        return URINALS[counter['val'] % len(URINALS)] if URINALS else match.group(0)
    elif 'kitchen' in url:
        return KITCHEN[counter['val'] % len(KITCHEN)] if KITCHEN else match.group(0)
    elif 'decorative' in url:
        return DECORATIVE if DECORATIVE else match.group(0)
    elif 'buffing' in url or 'polishing' in url:
        return BUFFING[counter['val'] % len(BUFFING)] if BUFFING else match.group(0)
    elif 'industrial' in url or 'industries' in url or 'medical' in url or 'health' in url:
        return INDUSTRIAL[counter['val'] % len(INDUSTRIAL)] if INDUSTRIAL else match.group(0)
    elif 'service' in url:
        return SERVICES[counter['val'] % len(SERVICES)] if SERVICES else match.group(0)
    elif 'before_after' in url or 'before%20after' in url:
        return BATHTUB_BEFORE[counter['val'] % len(BATHTUB_BEFORE)] if BATHTUB_BEFORE else match.group(0)
    elif 'warranty' in url:
        return BATHROOM[counter['val'] % len(BATHROOM)] if BATHROOM else match.group(0)
    elif 'bathroom' in url:
        return BATHROOM[counter['val'] % len(BATHROOM)] if BATHROOM else match.group(0)
    elif 'bathtub' in url or 'bath' in url:
        return BATHTUB_AFTER[counter['val'] % len(BATHTUB_AFTER)] if BATHTUB_AFTER else match.group(0)
    else:
        return BATHROOM[counter['val'] % len(BATHROOM)] if BATHROOM else match.group(0)

html = re.sub(old_cloudinary_pattern, replace_old_cloudinary, html)
print(f"   ✅ Old Cloudinary URLs replaced: {counter['val']}")

# 3. Replace local file paths
local_pattern = r'/Users/shyamkumarpandey/html/[^"\']+'
html = re.sub(local_pattern, HERO if HERO else '', html)
print(f"   ✅ Local file paths replaced")

# 4. Now set up specific sections with correct images

# Hero section - find and replace hero image
hero_section = r'(<img[^>]*alt="Luxury Modern Bathroom"[^>]*src=")[^"]+(")'
if HERO:
    html = re.sub(hero_section, f'\\1{HERO}\\2', html)

# Before/After section - update JavaScript arrays
# Find beforeImages array and replace
before_pattern = r"(const beforeImages = \[)[^\]]+(\])"
if BATHTUB_BEFORE:
    before_urls = ',\n            '.join([f'"{url}"' for url in BATHTUB_BEFORE])
    html = re.sub(before_pattern, f'\\1\n            {before_urls}\n        \\2', html)
    print(f"   ✅ Before images array updated ({len(BATHTUB_BEFORE)} images)")

after_pattern = r"(const afterImages = \[)[^\]]+(\])"
if BATHTUB_AFTER:
    after_urls = ',\n            '.join([f'"{url}"' for url in BATHTUB_AFTER])
    html = re.sub(after_pattern, f'\\1\n            {after_urls}\n        \\2', html)
    print(f"   ✅ After images array updated ({len(BATHTUB_AFTER)} images)")

# Save backup
backup_file = HTML_FILE + ".backup_finest_coating"
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(original_html)
print(f"\n💾 Backup saved: {backup_file}")

# Save updated HTML
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"✅ HTML file updated: {HTML_FILE}")

# Summary
print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print(f"   ✅ Total replacements made")
print(f"   📁 All images now from: Finest Coating/")
print("=" * 60)
print("\n🎉 Website now uses Finest Coating Cloudinary images!")
