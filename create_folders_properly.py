#!/usr/bin/env python3
"""
Create explicit folders in Cloudinary and reorganize images
"""

import cloudinary.api
import cloudinary.uploader
import cloudinary

cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg",
    secure=True
)

def create_folder(path):
    """Create a folder by uploading a dummy asset"""
    try:
        # Upload a tiny 1x1 transparent PNG to create the folder
        result = cloudinary.uploader.upload(
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            folder=path,
            public_id=".keep",
            overwrite=True,
            resource_type="image"
        )
        print(f"   ✅ Created: {path}/")
        return True
    except Exception as e:
        print(f"   ❌ Error creating {path}: {str(e)}")
        return False

def main():
    print("=" * 80)
    print("📁 CREATING FOLDER STRUCTURE IN CLOUDINARY")
    print("=" * 80)

    base = "Shyam/Finest Coating Shyam"

    folders_to_create = [
        # Main folders
        f"{base}/Gallery",
        f"{base}/Gallery/Before After",
        f"{base}/General",
        f"{base}/Industries",
        f"{base}/Industries/Ducting Pump Room",
        f"{base}/Industries/Hotels and Resorts",
        f"{base}/Industries/Multi-Surface Coating",
        f"{base}/Industries/Ships and Yachts",
        f"{base}/Industries/Waterslides",
        f"{base}/Services",
        f"{base}/Services/Bathtubs and Washbasins",
        f"{base}/Services/Buffing and Polishing",
        f"{base}/Services/Healthcare",
        f"{base}/Services/Industrial",
        f"{base}/Services/Kitchen",
        f"{base}/Services/Medical Equipment",
        f"{base}/Services/Urinals",
        f"{base}/Warranty",
    ]

    print("\n🔨 Creating folders...")
    print("-" * 80)

    created = 0
    for folder in folders_to_create:
        if create_folder(folder):
            created += 1

    print("-" * 80)
    print(f"\n✅ Created {created} folders")

    print("\n" + "=" * 80)
    print("✨ Now refresh Cloudinary console - folders should appear!")
    print("=" * 80)

if __name__ == "__main__":
    main()
