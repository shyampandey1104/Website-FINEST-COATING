#!/usr/bin/env python3
"""
HTML Image URL Updater Script
Ye script HTML file mein saari images ko Shyam/Finest_Coating/blue_color_website folder se replace karega.
"""

import re
import json

# Settings
HTML_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"
JSON_FILE = "/Users/shyamkumarpandey/html/cloudinary_urls.json"
OUTPUT_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"

# New Cloudinary base path
NEW_BASE = "Shyam/Finest_Coating/blue_color_website"

# Load uploaded URLs
with open(JSON_FILE, 'r') as f:
    uploaded_urls = json.load(f)

# Read HTML file
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html_content = f.read()

original_content = html_content

# Create mapping for different image categories
image_mappings = {
    # Bathroom images - use bathroom folder images
    'bathroom': [
        uploaded_urls.get("images/bathroom/images (1) (10).jpeg"),
        uploaded_urls.get("images/bathroom/images (31) (1).jpeg"),
        uploaded_urls.get("images/bathroom/images (25) (1).jpeg"),
        uploaded_urls.get("images/bathroom/images (24) (2).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (9).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (12).jpeg"),
        uploaded_urls.get("images/bathroom/images (8) (6).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (14).jpeg"),
        uploaded_urls.get("images/bathroom/images (4) (1).jpeg"),
        uploaded_urls.get("images/bathroom/images (23) (1).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (14) (1).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (13).jpeg"),
        uploaded_urls.get("images/bathroom/images (8) (7).jpeg"),
        uploaded_urls.get("images/bathroom/images (43).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (11) (1).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (6).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (20).jpeg"),
        uploaded_urls.get("images/bathroom/images (12) (5).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (8) (1).jpeg"),
        uploaded_urls.get("images/bathroom/images (1) (5).jpeg"),
        uploaded_urls.get("images/bathroom/images (7) (1).jpeg"),
    ],
    # Bathtub images
    'bathtub': [
        uploaded_urls.get("images/bathtub/bathtub-refinishing.png"),
        uploaded_urls.get("bathtub-after1.jpg"),
        uploaded_urls.get("bathtub-after2.jpg"),
        uploaded_urls.get("bathtub-after3.jpg"),
        uploaded_urls.get("bathtub-after4.jpg"),
        uploaded_urls.get("bathtub-after5.jpg"),
        uploaded_urls.get("bathtub-after6.jpg"),
        uploaded_urls.get("bathtub-before1.jpg"),
        uploaded_urls.get("bathtub-before2.jpg"),
        uploaded_urls.get("bathtub-before3.jpg"),
        uploaded_urls.get("bathtub-before4.jpg"),
        uploaded_urls.get("bathtub-before5.jpg"),
        uploaded_urls.get("bathtub-before6.jpg"),
    ],
    # Urinals images
    'urinals': [
        uploaded_urls.get("images/urinals/How-To-Keep-Urinals-Clean.jpg"),
        uploaded_urls.get("How-To-Keep-Urinals-Clean.jpg"),
        uploaded_urls.get("download.jpeg"),
        uploaded_urls.get("download1.jpeg"),
        uploaded_urls.get("download2.jpeg"),
        uploaded_urls.get("download3.jpeg"),
        uploaded_urls.get("images.jpeg"),
    ],
    # Kitchen images
    'kitchen': [
        uploaded_urls.get("images/kitchen/Gemini_Generated_Image_xw8bg5xw8bg5xw8b.png"),
        uploaded_urls.get("images/kitchen/Gemini_Generated_Image_ggp5esggp5esggp5.png"),
        uploaded_urls.get("kitchen1.jpeg"),
        uploaded_urls.get("kitchen2.jpeg"),
        uploaded_urls.get("kitchen3.jpeg"),
        uploaded_urls.get("kitchen4.jpg"),
        uploaded_urls.get("kitchen5.jpeg"),
    ],
    # Buffing images
    'buffing': [
        uploaded_urls.get("buffing1.jpeg"),
        uploaded_urls.get("buffing2.jpeg"),
        uploaded_urls.get("buffing3.jpeg"),
    ],
    # Industrial images
    'industrial': [url for key, url in uploaded_urls.items() if 'industrial' in key.lower()],
    # Decorative images
    'decorative': [
        uploaded_urls.get("images/decorative/decorative-items.jpeg"),
    ],
    # Services images
    'services': [url for key, url in uploaded_urls.items() if 'services' in key.lower()],
    # Hero images
    'hero': [
        uploaded_urls.get("images/hero_bathtub.png"),
        uploaded_urls.get("hero-bathtub.png"),
    ],
    # Benefits images
    'benefits': [
        uploaded_urls.get("benefits-image-2.jpeg"),
    ],
    # FAQ images
    'faq': [
        uploaded_urls.get("faq-image-2.jpeg"),
    ],
}

# Filter out None values
for key in image_mappings:
    image_mappings[key] = [url for url in image_mappings[key] if url]

print("=" * 60)
print("🔄 HTML Image URL Updater")
print("=" * 60)

replacements_made = 0

# 1. Replace Abdul Images URLs with Shyam folder URLs
print("\n📦 Replacing Abdul Images URLs...")

# Pattern to find Abdul Images URLs
abdul_pattern = r'https://res\.cloudinary\.com/dd2sbrcrr/image/upload/[^"\']+/Abdul%20Images/[^"\']+'

def get_replacement_url(match):
    global replacements_made
    old_url = match.group(0)

    # Extract category from URL
    url_lower = old_url.lower()

    if 'urinal' in url_lower:
        if image_mappings['urinals']:
            replacements_made += 1
            return image_mappings['urinals'][replacements_made % len(image_mappings['urinals'])]
    elif 'kitchen' in url_lower:
        if image_mappings['kitchen']:
            replacements_made += 1
            return image_mappings['kitchen'][replacements_made % len(image_mappings['kitchen'])]
    elif 'decorative' in url_lower:
        if image_mappings['decorative']:
            replacements_made += 1
            return image_mappings['decorative'][0]
    elif 'industrial' in url_lower or 'industries' in url_lower:
        if image_mappings['industrial']:
            replacements_made += 1
            return image_mappings['industrial'][replacements_made % len(image_mappings['industrial'])]
    elif 'buffing' in url_lower or 'polishing' in url_lower:
        if image_mappings['buffing']:
            replacements_made += 1
            return image_mappings['buffing'][replacements_made % len(image_mappings['buffing'])]
    elif 'bathroom' in url_lower:
        if image_mappings['bathroom']:
            replacements_made += 1
            return image_mappings['bathroom'][replacements_made % len(image_mappings['bathroom'])]
    elif 'bathtub' in url_lower or 'bath' in url_lower:
        if image_mappings['bathtub']:
            replacements_made += 1
            return image_mappings['bathtub'][replacements_made % len(image_mappings['bathtub'])]
    elif 'before_after' in url_lower or 'before%20after' in url_lower:
        if image_mappings['bathtub']:
            replacements_made += 1
            return image_mappings['bathtub'][replacements_made % len(image_mappings['bathtub'])]
    elif 'warranty' in url_lower:
        if image_mappings['bathroom']:
            replacements_made += 1
            return image_mappings['bathroom'][replacements_made % len(image_mappings['bathroom'])]
    elif 'health' in url_lower or 'medical' in url_lower:
        if image_mappings['industrial']:
            replacements_made += 1
            return image_mappings['industrial'][replacements_made % len(image_mappings['industrial'])]
    elif 'ship' in url_lower or 'yacht' in url_lower:
        if image_mappings['industrial']:
            replacements_made += 1
            return image_mappings['industrial'][replacements_made % len(image_mappings['industrial'])]
    elif 'waterslide' in url_lower or 'frp' in url_lower:
        if image_mappings['industrial']:
            replacements_made += 1
            return image_mappings['industrial'][replacements_made % len(image_mappings['industrial'])]
    elif 'ducting' in url_lower or 'pump' in url_lower:
        if image_mappings['industrial']:
            replacements_made += 1
            return image_mappings['industrial'][replacements_made % len(image_mappings['industrial'])]
    elif 'hotel' in url_lower or 'resort' in url_lower:
        if image_mappings['bathroom']:
            replacements_made += 1
            return image_mappings['bathroom'][replacements_made % len(image_mappings['bathroom'])]
    elif 'multi' in url_lower or 'surface' in url_lower:
        if image_mappings['industrial']:
            replacements_made += 1
            return image_mappings['industrial'][replacements_made % len(image_mappings['industrial'])]

    # Default: use bathroom or industrial images
    if image_mappings['bathroom']:
        replacements_made += 1
        return image_mappings['bathroom'][replacements_made % len(image_mappings['bathroom'])]

    return old_url

html_content = re.sub(abdul_pattern, get_replacement_url, html_content)
print(f"   ✅ Abdul Images URLs replaced: {replacements_made}")

# 2. Replace Unsplash URLs
print("\n📦 Replacing Unsplash URLs...")
unsplash_count = 0

unsplash_pattern = r'https://images\.unsplash\.com/[^"\']+'

def replace_unsplash(match):
    global unsplash_count
    unsplash_count += 1
    # Use bathtub or bathroom images for unsplash replacements
    if image_mappings['bathtub']:
        return image_mappings['bathtub'][unsplash_count % len(image_mappings['bathtub'])]
    elif image_mappings['bathroom']:
        return image_mappings['bathroom'][unsplash_count % len(image_mappings['bathroom'])]
    return match.group(0)

html_content = re.sub(unsplash_pattern, replace_unsplash, html_content)
print(f"   ✅ Unsplash URLs replaced: {unsplash_count}")

# 3. Replace local file paths
print("\n📦 Replacing local file paths...")
local_count = 0

# Replace fc_logo.png with a valid image (using hero image as logo placeholder)
logo_pattern = r'/Users/shyamkumarpandey/html/fc_logo\.png'
if image_mappings['hero']:
    html_content = re.sub(logo_pattern, image_mappings['hero'][0], html_content)
    local_count += 1
    print(f"   ✅ Logo path replaced")

print(f"   ✅ Local paths replaced: {local_count}")

# Save updated HTML
print("\n💾 Saving updated HTML file...")

# Create backup
backup_file = HTML_FILE + ".backup_before_update"
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(original_content)
print(f"   📋 Backup saved: {backup_file}")

# Save updated file
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"   ✅ HTML file updated: {OUTPUT_FILE}")

# Summary
print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print(f"   ✅ Abdul Images URLs replaced: {replacements_made}")
print(f"   ✅ Unsplash URLs replaced: {unsplash_count}")
print(f"   ✅ Local paths replaced: {local_count}")
print(f"   📁 Total replacements: {replacements_made + unsplash_count + local_count}")
print("=" * 60)
print("\n🎉 All images now point to Shyam/Finest_Coating/blue_color_website folder!")
