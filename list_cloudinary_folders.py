#!/usr/bin/env python3
"""
List all Cloudinary folders and images
"""

import cloudinary
import cloudinary.api

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

print("=" * 60)
print("📁 Cloudinary Folder List")
print("=" * 60)

try:
    # List root folders
    print("\n📂 Root folders:")
    result = cloudinary.api.root_folders()
    for folder in result.get('folders', []):
        print(f"   • {folder['name']}")

    # Check Shyam folder
    print("\n📂 Shyam folder contents:")
    try:
        result = cloudinary.api.subfolders("Shyam")
        for folder in result.get('folders', []):
            print(f"   • Shyam/{folder['name']}")

            # Check subfolders
            try:
                sub_result = cloudinary.api.subfolders(f"Shyam/{folder['name']}")
                for sub in sub_result.get('folders', []):
                    print(f"      • Shyam/{folder['name']}/{sub['name']}")
            except:
                pass
    except Exception as e:
        print(f"   ⚠️  {str(e)}")

    # List resources in Shyam folder
    print("\n📷 Images in Shyam folder:")
    try:
        result = cloudinary.api.resources(
            type="upload",
            prefix="Shyam",
            max_results=500
        )
        count = 0
        for resource in result.get('resources', []):
            count += 1
            if count <= 20:
                print(f"   • {resource['public_id']}")
        if count > 20:
            print(f"   ... and {count - 20} more images")
        print(f"\n   Total images in Shyam: {count}")
    except Exception as e:
        print(f"   ⚠️  {str(e)}")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
