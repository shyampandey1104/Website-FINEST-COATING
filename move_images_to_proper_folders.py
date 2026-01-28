#!/usr/bin/env python3
"""
Move all images from old paths to proper organized folders
"""

import cloudinary.api
import cloudinary.uploader
import cloudinary
import json

cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg",
    secure=True
)

BASE_FOLDER = "Shyam/Finest Coating Shyam"

def get_all_images():
    """Get all images currently in Shyam/Finest Coating Shyam"""
    try:
        result = cloudinary.api.resources(
            type='upload',
            prefix=BASE_FOLDER,
            max_results=500
        )
        return result['resources']
    except Exception as e:
        print(f"Error: {e}")
        return []

def should_reorganize(public_id):
    """Check if this image needs to be reorganized"""
    # Skip .keep files
    if public_id.endswith('.keep'):
        return False

    # Skip test images
    if 'test_image' in public_id:
        return False

    # Check if already in proper structure
    parts = public_id.split('/')

    # Proper structure should be: Shyam/Finest Coating Shyam/[Section]/[Subsection]/filename
    # or: Shyam/Finest Coating Shyam/[Section]/filename

    if len(parts) >= 4:
        section = parts[2]  # Gallery, Services, Industries, etc.

        # If it's Services or Industries, should have subsection
        if section in ['Services', 'Industries']:
            if len(parts) >= 5:
                return False  # Already properly organized
            else:
                return True  # Needs subsection
        else:
            if len(parts) >= 4:
                return False  # Already organized

    return True

def categorize_image(public_id):
    """Determine correct folder for an image based on its current path"""
    pid_lower = public_id.lower()

    # Extract from current path or filename
    if 'gallery' in pid_lower and 'before' in pid_lower:
        return 'Gallery/Before After'
    elif 'general' in pid_lower:
        return 'General'
    elif 'ducting' in pid_lower or 'pump' in pid_lower:
        return 'Industries/Ducting Pump Room'
    elif 'hotel' in pid_lower or 'resort' in pid_lower:
        return 'Industries/Hotels and Resorts'
    elif 'multi' in pid_lower and 'surface' in pid_lower:
        return 'Industries/Multi-Surface Coating'
    elif 'ship' in pid_lower or 'yacht' in pid_lower:
        return 'Industries/Ships and Yachts'
    elif 'waterslide' in pid_lower:
        return 'Industries/Waterslides'
    elif 'bathtub' in pid_lower or 'washbasin' in pid_lower:
        return 'Services/Bathtubs and Washbasins'
    elif 'buffing' in pid_lower or 'polish' in pid_lower:
        return 'Services/Buffing and Polishing'
    elif 'healthcare' in pid_lower:
        return 'Services/Healthcare'
    elif 'industrial' in pid_lower or 'machinery' in pid_lower:
        return 'Services/Industrial'
    elif 'kitchen' in pid_lower:
        return 'Services/Kitchen'
    elif 'medical' in pid_lower or 'equipment' in pid_lower:
        return 'Services/Medical Equipment'
    elif 'urinal' in pid_lower:
        return 'Services/Urinals'
    elif 'warranty' in pid_lower or 'care' in pid_lower:
        return 'Warranty'
    else:
        return 'General'

def move_image(old_public_id, new_section):
    """Move/rename image to new folder"""

    # Get filename from old public_id
    filename = old_public_id.split('/')[-1]

    # Create new public_id
    new_public_id = f"{BASE_FOLDER}/{new_section}/{filename}"

    # Skip if already in correct location
    if old_public_id == new_public_id:
        return None

    try:
        print(f"   📦 Moving: {filename}")
        print(f"      From: {old_public_id}")
        print(f"      To:   {new_public_id}")

        result = cloudinary.uploader.rename(
            old_public_id,
            new_public_id,
            overwrite=True,
            invalidate=True
        )

        print(f"      ✅ Success\n")

        return {
            'old_public_id': old_public_id,
            'new_public_id': new_public_id,
            'new_url': result['secure_url'],
            'section': new_section
        }

    except Exception as e:
        print(f"      ❌ Error: {str(e)}\n")
        return None

def main():
    print("=" * 100)
    print("🔄 REORGANIZING IMAGES INTO PROPER FOLDERS")
    print("=" * 100)

    # Get all images
    print("\n📖 Fetching all images...")
    all_images = get_all_images()
    print(f"✅ Found {len(all_images)} total images\n")

    # Find images that need reorganization
    images_to_move = []
    for img in all_images:
        public_id = img['public_id']
        if should_reorganize(public_id):
            target_section = categorize_image(public_id)
            images_to_move.append({
                'public_id': public_id,
                'section': target_section
            })

    print(f"📊 Images to reorganize: {len(images_to_move)}\n")

    if len(images_to_move) == 0:
        print("✅ All images are already properly organized!")
        return

    # Show plan
    from collections import defaultdict
    by_section = defaultdict(int)
    for img in images_to_move:
        by_section[img['section']] += 1

    print("📋 Reorganization Plan:")
    print("-" * 100)
    for section, count in sorted(by_section.items()):
        print(f"   {section:<50} {count:>3} images")
    print("-" * 100)

    print("\n" + "=" * 100)
    print("🚀 Starting reorganization...")
    print("=" * 100 + "\n")

    results = {
        'moved': [],
        'failed': []
    }

    for img_info in images_to_move:
        result = move_image(img_info['public_id'], img_info['section'])
        if result:
            results['moved'].append(result)
        else:
            results['failed'].append(img_info)

    # Save results
    results_file = "/Users/shyamkumarpandey/html/reorganization_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Summary
    print("\n" + "=" * 100)
    print("📊 REORGANIZATION SUMMARY")
    print("=" * 100)
    print(f"✅ Successfully moved: {len(results['moved'])} images")
    print(f"❌ Failed: {len(results['failed'])} images")
    print(f"📄 Results saved to: {results_file}")
    print("=" * 100)

    print("\n✨ Done! Refresh Cloudinary console - images should now appear in folders!\n")

if __name__ == "__main__":
    main()
