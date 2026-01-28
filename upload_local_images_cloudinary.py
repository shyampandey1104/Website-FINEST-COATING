#!/usr/bin/env python3
"""
Upload all local images from HTML to Cloudinary
Extracts image paths from HTML and uploads them with proper folder structure
"""

import os
import re
import cloudinary
import cloudinary.uploader
from pathlib import Path
import json
from urllib.parse import urlparse

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = "dd2sbrcrr"
CLOUDINARY_API_KEY = "173777767114771"
CLOUDINARY_API_SECRET = "vcbZWirynnzsfWAlOgg-Jg6Xyqg"

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

# Paths
HTML_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"
WORKING_DIR = "/Users/shyamkumarpandey/html"
BASE_CLOUDINARY_FOLDER = "Abdul Images/Finest Coating"

def extract_local_images_from_html(html_file):
    """Extract all local image references from HTML file"""
    print(f"📖 Reading HTML file: {html_file}")

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all src attributes
    img_pattern = r'src=["\']([^"\']+)["\']'
    all_images = re.findall(img_pattern, content)

    # Filter local images only
    local_images = []
    for img in all_images:
        # Skip URLs
        if img.startswith(('http://', 'https://', '//', 'data:')):
            continue
        # Skip if already from cloudinary
        if 'cloudinary' in img.lower():
            continue
        # Skip if it's a relative path starting with /
        if img.startswith('/') and not os.path.exists(os.path.join(WORKING_DIR, img.lstrip('/'))):
            continue
        # Skip template variables like ${imageUrl}, ${img.url}
        if '${' in img or '{' in img or '}' in img:
            continue
        # Skip if doesn't have image extension
        if not img.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')):
            continue

        local_images.append(img)

    # Remove duplicates
    local_images = list(set(local_images))

    print(f"✅ Found {len(local_images)} unique local images\n")
    return local_images

def categorize_image(image_path):
    """Determine the category/folder for an image based on its name"""
    img_lower = image_path.lower()

    # Category mapping (without special characters like &)
    if 'bathtub' in img_lower or 'washbasin' in img_lower:
        return 'Bathtubs and Washbasins'
    elif 'urinal' in img_lower:
        return 'Urinals'
    elif 'kitchen' in img_lower:
        return 'Kitchen'
    elif 'buffing' in img_lower or 'polish' in img_lower:
        return 'Buffing and Polishing'
    elif 'medical' in img_lower or 'hospital' in img_lower or 'healthcare' in img_lower:
        return 'Healthcare'
    elif 'industrial' in img_lower or 'machinery' in img_lower or 'equipment' in img_lower:
        return 'Industrial'
    elif 'before' in img_lower:
        return 'Before After/Before'
    elif 'after' in img_lower:
        return 'Before After/After'
    else:
        # All miscellaneous images go to Urinals folder
        return 'Urinals'

def upload_to_cloudinary(local_path, category):
    """Upload a single image to Cloudinary"""

    # Full path to the file
    full_path = os.path.join(WORKING_DIR, local_path)

    # Check if file exists
    if not os.path.exists(full_path):
        print(f"   ❌ File not found: {full_path}")
        return None

    try:
        # Get filename and create public_id
        filename = Path(local_path).stem  # filename without extension

        # Create cloudinary folder path
        cloudinary_folder = f"{BASE_CLOUDINARY_FOLDER}/{category}"

        # Upload to Cloudinary
        print(f"   ⬆️  Uploading: {local_path}")
        result = cloudinary.uploader.upload(
            full_path,
            folder=cloudinary_folder,
            public_id=filename,
            overwrite=True,
            resource_type="image",
            invalidate=True
        )

        cloudinary_url = result['secure_url']
        print(f"   ✅ Success: {cloudinary_url}\n")

        return {
            'local_path': local_path,
            'category': category,
            'cloudinary_url': cloudinary_url,
            'public_id': result['public_id'],
            'format': result['format'],
            'width': result['width'],
            'height': result['height']
        }

    except Exception as e:
        print(f"   ❌ Error: {str(e)}\n")
        return None

def main():
    print("=" * 80)
    print("🚀 CLOUDINARY UPLOADER - Finest Coating Website")
    print("=" * 80)
    print(f"Cloud Name: {CLOUDINARY_CLOUD_NAME}")
    print(f"HTML File: {HTML_FILE}")
    print(f"Working Directory: {WORKING_DIR}")
    print("=" * 80)

    # Step 1: Extract local images from HTML
    local_images = extract_local_images_from_html(HTML_FILE)

    if not local_images:
        print("⚠️  No local images found in HTML file!")
        return

    # Step 2: Categorize images
    print("\n📂 Categorizing images...")
    categorized = {}
    for img in local_images:
        category = categorize_image(img)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(img)

    # Display categorization
    print("\n📊 Image Categories:")
    total_count = 0
    for category, images in sorted(categorized.items()):
        count = len(images)
        total_count += count
        print(f"   • {category}: {count} images")
    print(f"   TOTAL: {total_count} images")

    # Step 3: Display sample images
    print("\n📸 Sample images to upload:")
    for i, img in enumerate(local_images[:10], 1):
        print(f"   {i}. {img}")
    if len(local_images) > 10:
        print(f"   ... and {len(local_images) - 10} more")

    # Step 4: Ask for confirmation (auto-proceed)
    print("\n" + "=" * 80)
    print("✅ Auto-proceeding with upload...")
    # response = input("🤔 Proceed with upload to Cloudinary? (yes/no): ").strip().lower()
    # if response not in ['yes', 'y']:
    #     print("❌ Upload cancelled by user")
    #     return

    # Step 5: Upload images
    print("\n" + "=" * 80)
    print("📤 Starting upload...")
    print("=" * 80 + "\n")

    results = {
        'uploaded': [],
        'failed': []
    }

    for category, images in sorted(categorized.items()):
        print(f"📁 Category: {category}")
        print("-" * 80)

        for img in images:
            result = upload_to_cloudinary(img, category)
            if result:
                results['uploaded'].append(result)
            else:
                results['failed'].append({
                    'local_path': img,
                    'category': category,
                    'reason': 'Upload failed'
                })

    # Step 6: Save results
    results_file = os.path.join(WORKING_DIR, 'cloudinary_upload_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Step 7: Summary
    print("\n" + "=" * 80)
    print("📊 UPLOAD SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully uploaded: {len(results['uploaded'])} images")
    print(f"❌ Failed: {len(results['failed'])} images")
    print(f"📄 Results saved to: {results_file}")
    print("=" * 80)

    # Show some uploaded URLs
    if results['uploaded']:
        print("\n📸 Sample Cloudinary URLs:")
        for result in results['uploaded'][:5]:
            print(f"\n   Local: {result['local_path']}")
            print(f"   Cloud: {result['cloudinary_url']}")

    # Show failed uploads
    if results['failed']:
        print("\n⚠️  Failed uploads:")
        for failed in results['failed']:
            print(f"   • {failed['local_path']} - {failed['reason']}")

    print("\n✨ Done!\n")

if __name__ == "__main__":
    main()
