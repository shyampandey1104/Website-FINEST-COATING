#!/usr/bin/env python3
"""
Cloudinary Image Delete Script
Ye script Shyam/Finest_Coating/blue_color_website folder ki saari images delete karega.
"""

import cloudinary
import cloudinary.api

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

# Folder to delete
FOLDER_TO_DELETE = "Shyam/Finest_Coating/blue_color_website"

print("=" * 60)
print("🗑️  Cloudinary Image Delete Script")
print("=" * 60)
print(f"\n📁 Folder to delete: {FOLDER_TO_DELETE}")
print("-" * 60)

try:
    # First, delete all resources in the folder
    print("\n🔍 Finding all images in folder...")

    # Get all resources in the folder and subfolders
    deleted_count = 0

    # Delete resources by prefix
    print("\n🗑️  Deleting all images...")

    result = cloudinary.api.delete_resources_by_prefix(
        FOLDER_TO_DELETE,
        resource_type="image"
    )

    if result.get('deleted'):
        deleted_count = len(result['deleted'])
        print(f"   ✅ Deleted {deleted_count} images")

    # Also try to delete from subfolders
    subfolders = ['bathroom', 'bathtub', 'decorative', 'industrial', 'kitchen', 'services', 'urinals']

    for subfolder in subfolders:
        try:
            sub_result = cloudinary.api.delete_resources_by_prefix(
                f"{FOLDER_TO_DELETE}/{subfolder}",
                resource_type="image"
            )
            if sub_result.get('deleted'):
                sub_deleted = len(sub_result['deleted'])
                deleted_count += sub_deleted
                print(f"   ✅ Deleted {sub_deleted} images from {subfolder}/")
        except Exception as e:
            pass

    # Now delete the empty folders
    print("\n🗑️  Deleting empty folders...")

    # Delete subfolders first
    for subfolder in subfolders:
        try:
            cloudinary.api.delete_folder(f"{FOLDER_TO_DELETE}/{subfolder}")
            print(f"   ✅ Deleted folder: {subfolder}/")
        except Exception as e:
            pass

    # Delete main folder
    try:
        cloudinary.api.delete_folder(FOLDER_TO_DELETE)
        print(f"   ✅ Deleted main folder: {FOLDER_TO_DELETE}")
    except Exception as e:
        print(f"   ⚠️  Could not delete main folder: {str(e)}")

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"   🗑️  Total images deleted: {deleted_count}")
    print(f"   📁 Folder deleted: {FOLDER_TO_DELETE}")
    print("=" * 60)
    print("\n✅ Done! Cloudinary folder has been cleaned up.")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
