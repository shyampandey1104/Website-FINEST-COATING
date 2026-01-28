#!/usr/bin/env python3
"""
Delete ALL images from Home/root folder in Cloudinary
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
print("🗑️  Delete ALL Images from Cloudinary Home")
print("=" * 60)

total_deleted = 0

# List root folders first
print("\n📂 Root folders in Cloudinary:")
try:
    result = cloudinary.api.root_folders()
    for folder in result.get('folders', []):
        print(f"   • {folder['name']}")
except Exception as e:
    print(f"   ⚠️  {str(e)}")

# Delete ALL images from the account
print("\n🗑️  Deleting ALL images from Cloudinary...")

try:
    while True:
        # Get all resources
        result = cloudinary.api.resources(
            type="upload",
            max_results=100
        )

        resources = result.get('resources', [])
        if not resources:
            break

        # Get public_ids
        public_ids = [r['public_id'] for r in resources]

        # Show what we're deleting
        for pid in public_ids[:5]:
            print(f"   Deleting: {pid}")
        if len(public_ids) > 5:
            print(f"   ... and {len(public_ids) - 5} more")

        # Delete them
        delete_result = cloudinary.api.delete_resources(public_ids)

        deleted = len([k for k, v in delete_result.get('deleted', {}).items() if v == 'deleted'])
        total_deleted += deleted
        print(f"   ✅ Deleted batch of {deleted} images... (Total: {total_deleted})")

except Exception as e:
    print(f"   ⚠️  Error: {str(e)}")

print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print(f"   🗑️  Total images deleted: {total_deleted}")
print("=" * 60)
print("\n✅ Done! All images have been deleted from Cloudinary.")
