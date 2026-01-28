#!/usr/bin/env python3
"""
Move Miscellaneous images to Urinals folder on Cloudinary
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
import json

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

BASE_FOLDER = "Abdul Images/Finest Coating"

def main():
    print("=" * 80)
    print("📦 MOVE MISCELLANEOUS IMAGES TO URINALS FOLDER")
    print("=" * 80)

    # Load the upload results to see which images were in Miscellaneous
    results_file = "/Users/shyamkumarpandey/html/cloudinary_upload_results.json"

    print(f"\n📖 Loading upload results from: {results_file}")
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Find Miscellaneous images
    misc_images = [img for img in results['uploaded'] if img['category'] == 'Miscellaneous']

    print(f"✅ Found {len(misc_images)} images in Miscellaneous category\n")

    if not misc_images:
        print("⚠️  No miscellaneous images to move!")
        return

    # Display images to move
    print("📸 Images to move to Urinals folder:")
    for img in misc_images:
        print(f"   • {img['local_path']}")

    print("\n" + "=" * 80)
    print("🔄 Starting move operation...")
    print("=" * 80 + "\n")

    moved_images = []

    for img in misc_images:
        old_public_id = img['public_id']
        filename = img['local_path'].split('.')[0]  # Get filename without extension
        new_public_id = f"{BASE_FOLDER}/Urinals/{filename}"

        print(f"📦 Moving: {img['local_path']}")
        print(f"   From: {old_public_id}")
        print(f"   To:   {new_public_id}")

        try:
            # Rename/move the image in Cloudinary
            result = cloudinary.uploader.rename(
                old_public_id,
                new_public_id,
                overwrite=True,
                invalidate=True
            )

            new_url = result['secure_url']
            print(f"   ✅ Success: {new_url}\n")

            moved_images.append({
                'local_path': img['local_path'],
                'old_url': img['cloudinary_url'],
                'new_url': new_url,
                'old_public_id': old_public_id,
                'new_public_id': new_public_id
            })

        except Exception as e:
            print(f"   ❌ Error: {str(e)}\n")

    # Update the results file
    print("=" * 80)
    print("📝 Updating results file...")
    print("=" * 80)

    # Update categories and URLs in results
    for img in results['uploaded']:
        for moved in moved_images:
            if img['local_path'] == moved['local_path']:
                img['category'] = 'Urinals'
                img['cloudinary_url'] = moved['new_url']
                img['public_id'] = moved['new_public_id']

    # Save updated results
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results file updated\n")

    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"Total images moved: {len(moved_images)}")
    print(f"Destination: {BASE_FOLDER}/Urinals/")
    print("=" * 80)

    if moved_images:
        print("\n📸 Sample new URLs:")
        for moved in moved_images[:3]:
            print(f"\n   {moved['local_path']}")
            print(f"   Old: {moved['old_url']}")
            print(f"   New: {moved['new_url']}")

    print("\n✨ Done!\n")

if __name__ == "__main__":
    main()
