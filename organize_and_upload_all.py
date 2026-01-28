#!/usr/bin/env python3
"""
Comprehensive script to:
1. Extract ALL images from HTML file
2. Categorize them by section (Home, Services, About, etc.)
3. Upload to Cloudinary with proper folder structure: Shyam/Finest Coating/[Section]/
"""

import os
import re
import json
import cloudinary
import cloudinary.uploader
from pathlib import Path
from collections import defaultdict

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = "dd2sbrcrr"
CLOUDINARY_API_KEY = "173777767114771"
CLOUDINARY_API_SECRET = "vcbZWirynnzsfWAlOgg-Jg6Xyqg"

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

# Paths
HTML_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"
WORKING_DIR = "/Users/shyamkumarpandey/html"
BASE_CLOUDINARY_FOLDER = "Shyam/Finest Coating"

def extract_all_images_with_context(html_file):
    """Extract ALL images from HTML with their context/section"""
    print(f"📖 Reading HTML file: {html_file}")

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all img tags with src
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
    all_img_tags = re.findall(img_pattern, content)

    # Also find src attributes separately
    src_pattern = r'src=["\']([^"\']+)["\']'
    all_src = re.findall(src_pattern, content)

    # Combine and deduplicate
    all_images = list(set(all_img_tags + all_src))

    print(f"✅ Found {len(all_images)} total image references\n")
    return all_images

def categorize_by_section(image_path):
    """Categorize image by detecting which section it belongs to"""
    img_lower = image_path.lower()

    # Hero/Home section
    if any(x in img_lower for x in ['hero', 'banner', 'home', 'main']):
        return 'Home'

    # Services sections
    elif any(x in img_lower for x in ['bathtub', 'washbasin', 'tub']):
        return 'Services/Bathtubs and Washbasins'
    elif 'urinal' in img_lower:
        return 'Services/Urinals'
    elif 'kitchen' in img_lower:
        return 'Services/Kitchen'
    elif any(x in img_lower for x in ['buffing', 'polish']):
        return 'Services/Buffing and Polishing'
    elif any(x in img_lower for x in ['medical', 'hospital', 'healthcare']):
        return 'Services/Healthcare'
    elif any(x in img_lower for x in ['industrial', 'machinery', 'equipment']):
        return 'Services/Industrial'

    # Before/After
    elif 'before' in img_lower and 'after' in img_lower:
        return 'Before After'
    elif 'before' in img_lower:
        return 'Before After/Before'
    elif 'after' in img_lower:
        return 'Before After/After'

    # About section
    elif any(x in img_lower for x in ['about', 'team', 'company']):
        return 'About'

    # Benefits
    elif 'benefit' in img_lower:
        return 'Benefits'

    # Process
    elif 'process' in img_lower:
        return 'Process'

    # Gallery
    elif 'gallery' in img_lower:
        return 'Gallery'

    # FAQ
    elif 'faq' in img_lower:
        return 'FAQ'

    # Contact
    elif 'contact' in img_lower:
        return 'Contact'

    # Testimonials/Clients
    elif any(x in img_lower for x in ['client', 'testimonial', 'review']):
        return 'Clients'

    # Warranty/Care
    elif any(x in img_lower for x in ['warranty', 'care']):
        return 'Warranty'

    # Icons/UI elements
    elif any(x in img_lower for x in ['icon', 'logo', 'ui']):
        return 'Assets/Icons'

    # Default
    else:
        return 'General'

def filter_images(all_images):
    """Filter out URLs, data URIs, and keep only local images"""
    local_images = []

    for img in all_images:
        # Skip URLs
        if img.startswith(('http://', 'https://', '//', 'data:')):
            continue
        # Skip cloudinary (already uploaded)
        if 'cloudinary' in img.lower():
            continue
        # Skip template variables
        if '${' in img or '{' in img or '}' in img:
            continue
        # Only image files
        if not img.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico')):
            continue
        # Check if file exists
        full_path = os.path.join(WORKING_DIR, img)
        if not os.path.exists(full_path):
            continue

        local_images.append(img)

    return list(set(local_images))

def upload_image(local_path, section_folder):
    """Upload single image to Cloudinary"""
    full_path = os.path.join(WORKING_DIR, local_path)

    if not os.path.exists(full_path):
        return None

    try:
        filename = Path(local_path).stem
        cloudinary_folder = f"{BASE_CLOUDINARY_FOLDER}/{section_folder}"

        print(f"   ⬆️  {local_path} → {section_folder}/")

        result = cloudinary.uploader.upload(
            full_path,
            folder=cloudinary_folder,
            public_id=filename,
            overwrite=True,
            resource_type="image",
            invalidate=True
        )

        print(f"   ✅ {result['secure_url']}\n")

        return {
            'local_path': local_path,
            'section': section_folder,
            'cloudinary_url': result['secure_url'],
            'public_id': result['public_id'],
            'format': result.get('format'),
            'width': result.get('width'),
            'height': result.get('height')
        }

    except Exception as e:
        print(f"   ❌ Error: {str(e)}\n")
        return None

def main():
    print("=" * 90)
    print("🚀 COMPREHENSIVE CLOUDINARY UPLOADER - FINEST COATING")
    print("=" * 90)
    print(f"Cloud Name: {CLOUDINARY_CLOUD_NAME}")
    print(f"Base Folder: {BASE_CLOUDINARY_FOLDER}")
    print("=" * 90)

    # Step 1: Extract all images
    all_images = extract_all_images_with_context(HTML_FILE)

    # Step 2: Filter local images only
    print("\n🔍 Filtering local images...")
    local_images = filter_images(all_images)
    print(f"✅ Found {len(local_images)} local images to upload\n")

    if not local_images:
        print("⚠️  No local images found!")
        return

    # Step 3: Categorize by section
    print("📂 Categorizing images by section...")
    categorized = defaultdict(list)

    for img in local_images:
        section = categorize_by_section(img)
        categorized[section].append(img)

    # Display organization
    print("\n📊 Image Organization:")
    print("-" * 90)
    total = 0
    for section in sorted(categorized.keys()):
        count = len(categorized[section])
        total += count
        print(f"   📁 {section:<40} {count:>3} images")
    print("-" * 90)
    print(f"   TOTAL: {total} images\n")

    # Step 4: Display sample images
    print("📸 Sample images:")
    for i, img in enumerate(local_images[:15], 1):
        section = categorize_by_section(img)
        print(f"   {i:2}. {img:<40} → {section}")
    if len(local_images) > 15:
        print(f"   ... and {len(local_images) - 15} more\n")

    # Step 5: Upload
    print("=" * 90)
    print("✅ Starting upload...")
    print("=" * 90 + "\n")

    results = {
        'uploaded': [],
        'failed': []
    }

    for section in sorted(categorized.keys()):
        print(f"📁 Section: {section}")
        print("-" * 90)

        for img in categorized[section]:
            result = upload_image(img, section)
            if result:
                results['uploaded'].append(result)
            else:
                results['failed'].append({
                    'local_path': img,
                    'section': section
                })

    # Step 6: Save results
    results_file = os.path.join(WORKING_DIR, 'shyam_cloudinary_upload_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Summary
    print("\n" + "=" * 90)
    print("📊 UPLOAD SUMMARY")
    print("=" * 90)
    print(f"✅ Successfully uploaded: {len(results['uploaded'])} images")
    print(f"❌ Failed: {len(results['failed'])} images")
    print(f"📄 Results saved to: {results_file}")

    # Show folder structure
    print("\n📁 Cloudinary Folder Structure:")
    print("-" * 90)
    sections_uploaded = defaultdict(int)
    for img in results['uploaded']:
        sections_uploaded[img['section']] += 1

    for section in sorted(sections_uploaded.keys()):
        print(f"   {BASE_CLOUDINARY_FOLDER}/{section}/  ({sections_uploaded[section]} images)")

    print("=" * 90)
    print("\n✨ Done!\n")

if __name__ == "__main__":
    main()
