#!/usr/bin/env python3
"""
Reorganize existing Cloudinary images into proper folder structure:
Shyam/Finest Coating/[Section]/
"""

import re
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
from collections import defaultdict
from urllib.parse import unquote

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

HTML_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"
NEW_BASE_FOLDER = "Shyam/Finest Coating"

def extract_cloudinary_images(html_file):
    """Extract all Cloudinary image URLs from HTML"""
    print(f"📖 Reading HTML file: {html_file}")

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Cloudinary URLs
    pattern = r'https://res\.cloudinary\.com/dd2sbrcrr/image/upload/[^"\'\s]+'
    urls = re.findall(pattern, content)

    # Deduplicate
    urls = list(set(urls))

    print(f"✅ Found {len(urls)} unique Cloudinary images\n")
    return urls

def extract_public_id_from_url(url):
    """Extract public_id from Cloudinary URL"""
    # URL format: https://res.cloudinary.com/dd2sbrcrr/image/upload/v1234567890/folder/image.jpg
    # public_id: folder/image (without extension)

    # Decode URL
    url = unquote(url)

    # Remove base URL and version
    match = re.search(r'/upload/v\d+/(.+)$', url)
    if not match:
        match = re.search(r'/upload/(.+)$', url)

    if match:
        path = match.group(1)
        # Remove extension
        if '.' in path:
            path = path.rsplit('.', 1)[0]
        return path

    return None

def categorize_by_url(url):
    """Determine section based on URL content"""
    url_lower = url.lower()

    # Check existing folder structure
    if 'bathtub' in url_lower or 'washbasin' in url_lower:
        return 'Services/Bathtubs and Washbasins'
    elif 'urinal' in url_lower:
        return 'Services/Urinals'
    elif 'kitchen' in url_lower:
        return 'Services/Kitchen'
    elif 'buffing' in url_lower or 'polish' in url_lower:
        return 'Services/Buffing and Polishing'
    elif 'healthcare' in url_lower or 'medical' in url_lower or 'hospital' in url_lower:
        return 'Services/Healthcare'
    elif 'industrial' in url_lower or 'machinery' in url_lower or 'equipment' in url_lower:
        return 'Services/Industrial'
    elif 'before' in url_lower and 'after' not in url_lower:
        return 'Before After/Before'
    elif 'after' in url_lower and 'before' not in url_lower:
        return 'Before After/After'
    elif 'before' in url_lower or 'after' in url_lower:
        return 'Before After'
    elif 'about' in url_lower:
        return 'About'
    elif 'benefit' in url_lower:
        return 'Benefits'
    elif 'process' in url_lower:
        return 'Process'
    elif 'gallery' in url_lower:
        return 'Gallery'
    elif 'faq' in url_lower:
        return 'FAQ'
    elif 'contact' in url_lower:
        return 'Contact'
    elif 'client' in url_lower or 'testimonial' in url_lower:
        return 'Clients'
    elif 'warranty' in url_lower or 'care' in url_lower:
        return 'Warranty'
    elif 'hero' in url_lower or 'banner' in url_lower:
        return 'Home'
    else:
        return 'General'

def copy_to_new_structure(url, new_section):
    """Copy image to new folder structure on Cloudinary"""

    old_public_id = extract_public_id_from_url(url)
    if not old_public_id:
        return None

    # Extract filename from old public_id
    filename = old_public_id.split('/')[-1]

    # Create new public_id
    new_public_id = f"{NEW_BASE_FOLDER}/{new_section}/{filename}"

    try:
        # Use upload with URL to copy the image
        print(f"   📦 Copying: {filename}")
        print(f"      From: {old_public_id}")
        print(f"      To:   {new_public_id}")

        result = cloudinary.uploader.upload(
            url,
            public_id=new_public_id,
            overwrite=True,
            invalidate=True,
            resource_type="image"
        )

        new_url = result['secure_url']
        print(f"      ✅ Success: {new_url}\n")

        return {
            'old_url': url,
            'new_url': new_url,
            'old_public_id': old_public_id,
            'new_public_id': new_public_id,
            'section': new_section,
            'filename': filename
        }

    except Exception as e:
        print(f"      ❌ Error: {str(e)}\n")
        return None

def main():
    print("=" * 100)
    print("🔄 REORGANIZE CLOUDINARY IMAGES - NEW FOLDER STRUCTURE")
    print("=" * 100)
    print(f"New Base Folder: {NEW_BASE_FOLDER}")
    print("=" * 100)

    # Step 1: Extract Cloudinary URLs
    urls = extract_cloudinary_images(HTML_FILE)

    if not urls:
        print("⚠️  No Cloudinary images found!")
        return

    # Step 2: Categorize
    print("\n📂 Categorizing images...")
    categorized = defaultdict(list)

    for url in urls:
        section = categorize_by_url(url)
        categorized[section].append(url)

    # Display organization
    print("\n📊 Image Organization Plan:")
    print("-" * 100)
    total = 0
    for section in sorted(categorized.keys()):
        count = len(categorized[section])
        total += count
        print(f"   📁 {section:<50} {count:>3} images")
    print("-" * 100)
    print(f"   TOTAL: {total} images\n")

    # Ask to proceed
    print("=" * 100)
    print("✅ Starting reorganization...")
    print("=" * 100 + "\n")

    results = {
        'copied': [],
        'failed': []
    }

    # Step 3: Copy images
    for section in sorted(categorized.keys()):
        print(f"📁 Section: {section}")
        print("-" * 100)

        for url in categorized[section]:
            result = copy_to_new_structure(url, section)
            if result:
                results['copied'].append(result)
            else:
                results['failed'].append({
                    'url': url,
                    'section': section
                })

    # Step 4: Save results
    results_file = "/Users/shyamkumarpandey/html/reorganized_images.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Summary
    print("\n" + "=" * 100)
    print("📊 REORGANIZATION SUMMARY")
    print("=" * 100)
    print(f"✅ Successfully copied: {len(results['copied'])} images")
    print(f"❌ Failed: {len(results['failed'])} images")
    print(f"📄 Results saved to: {results_file}")

    # Show new folder structure
    print("\n📁 New Cloudinary Folder Structure:")
    print("-" * 100)
    sections_count = defaultdict(int)
    for img in results['copied']:
        sections_count[img['section']] += 1

    for section in sorted(sections_count.keys()):
        print(f"   {NEW_BASE_FOLDER}/{section}/  ({sections_count[section]} images)")

    print("=" * 100)
    print("\n✨ Done! Images are now organized in new folder structure.\n")
    print("⚠️  Note: Old images still exist. You may want to delete them manually from Cloudinary.\n")

if __name__ == "__main__":
    main()
