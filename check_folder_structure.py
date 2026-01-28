#!/usr/bin/env python3
"""
Check exact folder structure in Cloudinary
"""

import cloudinary.api
import cloudinary

cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg",
    secure=True
)

def check_subfolders(path):
    """Check subfolders in a path"""
    try:
        result = cloudinary.api.subfolders(path)
        return result['folders']
    except Exception as e:
        return []

def main():
    print("=" * 80)
    print("📁 CHECKING FOLDER STRUCTURE")
    print("=" * 80)

    # Check Shyam folder
    print("\n1. Checking 'Shyam' folder:")
    shyam_folders = check_subfolders("Shyam")
    if shyam_folders:
        for folder in shyam_folders:
            print(f"   ✅ {folder['name']}")
    else:
        print("   ❌ No subfolders found")

    # Check Shyam/Finest Coating Shyam
    print("\n2. Checking 'Shyam/Finest Coating Shyam' folder:")
    fc_folders = check_subfolders("Shyam/Finest Coating Shyam")
    if fc_folders:
        for folder in fc_folders:
            print(f"   ✅ {folder['name']}")

            # Check subfolders
            subfolder_path = f"Shyam/Finest Coating Shyam/{folder['name']}"
            subfolders = check_subfolders(subfolder_path)
            if subfolders:
                for sf in subfolders:
                    print(f"      └─ {sf['name']}")
    else:
        print("   ❌ No subfolders found")

    # List actual resources
    print("\n3. Checking actual images:")
    result = cloudinary.api.resources(
        type='upload',
        prefix='Shyam/Finest Coating Shyam',
        max_results=10
    )

    print(f"   Total images: {len(result['resources'])}")
    print("\n   Sample images:")
    for img in result['resources'][:5]:
        print(f"   • {img['public_id']}")

if __name__ == "__main__":
    main()
