#!/usr/bin/env python3
"""
Upload all website images to Shyam/Finest Coating Shyam/ with proper organization
"""

import re
import json
import cloudinary
import cloudinary.uploader
from collections import defaultdict

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg",
    secure=True
)

HTML_FILE = "/Users/shyamkumarpandey/html/blue_color_website.html"
NEW_BASE_FOLDER = "Shyam/Finest Coating Shyam"

def extract_cloudinary_images(html_file):
    """Extract all Cloudinary image URLs from HTML"""
    print(f"📖 Reading HTML file...")

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Cloudinary URLs
    pattern = r'https://res\.cloudinary\.com/dd2sbrcrr/image/upload/[^"\'\s]+'
    urls = re.findall(pattern, content)

    # Deduplicate
    urls = list(set(urls))

    print(f"✅ Found {len(urls)} unique Cloudinary images\n")
    return urls

def categorize_by_content(url):
    """Categorize image by URL content"""
    url_lower = url.lower()

    # Services sections
    if 'bathtub' in url_lower or 'washbasin' in url_lower:
        return 'Services/Bathtubs and Washbasins'
    elif 'urinal' in url_lower:
        return 'Services/Urinals'
    elif 'kitchen' in url_lower:
        return 'Services/Kitchen'
    elif 'buffing' in url_lower or 'polish' in url_lower:
        return 'Services/Buffing and Polishing'
    elif 'healthcare' in url_lower or 'health' in url_lower:
        return 'Services/Healthcare'
    elif 'medical' in url_lower:
        return 'Services/Medical Equipment'
    elif 'industrial' in url_lower or 'machinery' in url_lower or 'equipment' in url_lower:
        return 'Services/Industrial'

    # Industries sections
    elif 'ducting' in url_lower or 'pump' in url_lower:
        return 'Industries/Ducting Pump Room'
    elif 'waterslide' in url_lower or 'water' in url_lower and 'slide' in url_lower:
        return 'Industries/Waterslides'
    elif 'hotel' in url_lower or 'resort' in url_lower:
        return 'Industries/Hotels and Resorts'
    elif 'ship' in url_lower or 'yacht' in url_lower:
        return 'Industries/Ships and Yachts'
    elif 'multi' in url_lower and 'surface' in url_lower:
        return 'Industries/Multi-Surface Coating'

    # General sections
    elif 'before' in url_lower and 'after' not in url_lower:
        return 'Gallery/Before After/Before'
    elif 'after' in url_lower and 'before' not in url_lower:
        return 'Gallery/Before After/After'
    elif 'before' in url_lower or 'after' in url_lower:
        return 'Gallery/Before After'
    elif 'gallery' in url_lower:
        return 'Gallery'
    elif 'about' in url_lower:
        return 'About'
    elif 'benefit' in url_lower:
        return 'Benefits'
    elif 'process' in url_lower:
        return 'Process'
    elif 'faq' in url_lower:
        return 'FAQ'
    elif 'contact' in url_lower:
        return 'Contact'
    elif 'warranty' in url_lower or 'care' in url_lower:
        return 'Warranty'
    elif 'hero' in url_lower or 'banner' in url_lower:
        return 'Home'
    else:
        return 'General'

def extract_filename_from_url(url):
    """Extract clean filename from Cloudinary URL"""
    # Get the last part after the last /
    parts = url.split('/')
    filename_with_ext = parts[-1]

    # Remove extension
    if '.' in filename_with_ext:
        filename = filename_with_ext.rsplit('.', 1)[0]
    else:
        filename = filename_with_ext

    return filename

def copy_image_to_new_folder(url, section):
    """Copy image from old location to new Shyam folder"""

    filename = extract_filename_from_url(url)
    new_public_id = f"{NEW_BASE_FOLDER}/{section}/{filename}"

    try:
        print(f"   📦 {filename}")
        print(f"      → {section}/")

        # Upload from existing URL to new location
        result = cloudinary.uploader.upload(
            url,
            public_id=new_public_id,
            overwrite=True,
            invalidate=True,
            resource_type="image"
        )

        new_url = result['secure_url']
        print(f"      ✅ {new_url}\n")

        return {
            'old_url': url,
            'new_url': new_url,
            'new_public_id': new_public_id,
            'section': section,
            'filename': filename
        }

    except Exception as e:
        print(f"      ❌ Error: {str(e)}\n")
        return None

def main():
    print("=" * 100)
    print("🚀 UPLOAD ALL IMAGES TO: Shyam/Finest Coating Shyam/")
    print("=" * 100)

    # Extract all Cloudinary images
    urls = extract_cloudinary_images(HTML_FILE)

    if not urls:
        print("⚠️  No Cloudinary images found!")
        return

    # Categorize images
    print("\n📂 Categorizing images by section...")
    categorized = defaultdict(list)

    for url in urls:
        section = categorize_by_content(url)
        categorized[section].append(url)

    # Display organization plan
    print("\n📊 Upload Plan:")
    print("-" * 100)
    total = 0
    for section in sorted(categorized.keys()):
        count = len(categorized[section])
        total += count
        print(f"   📁 {section:<50} {count:>3} images")
    print("-" * 100)
    print(f"   TOTAL: {total} images\n")

    # Start upload
    print("=" * 100)
    print("📤 Starting upload to Shyam/Finest Coating Shyam/...")
    print("=" * 100 + "\n")

    results = {
        'uploaded': [],
        'failed': []
    }

    for section in sorted(categorized.keys()):
        print(f"📁 Section: {section}")
        print("-" * 100)

        for url in categorized[section]:
            result = copy_image_to_new_folder(url, section)
            if result:
                results['uploaded'].append(result)
            else:
                results['failed'].append({
                    'url': url,
                    'section': section
                })

    # Save results
    results_file = "/Users/shyamkumarpandey/html/shyam_folder_upload_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Summary
    print("\n" + "=" * 100)
    print("📊 UPLOAD SUMMARY")
    print("=" * 100)
    print(f"✅ Successfully uploaded: {len(results['uploaded'])} images")
    print(f"❌ Failed: {len(results['failed'])} images")
    print(f"📄 Results saved to: {results_file}")

    # Show folder structure
    print("\n📁 Cloudinary Folder Structure:")
    print("-" * 100)
    sections_count = defaultdict(int)
    for img in results['uploaded']:
        sections_count[img['section']] += 1

    for section in sorted(sections_count.keys()):
        print(f"   {NEW_BASE_FOLDER}/{section}/  ({sections_count[section]} images)")

    print("=" * 100)
    print("\n✨ Done! Check Cloudinary console - Shyam/Finest Coating Shyam/ folder!\n")

if __name__ == "__main__":
    main()
