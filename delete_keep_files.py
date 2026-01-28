#!/usr/bin/env python3
"""
Delete all .keep files from folders so actual images can be seen
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

def main():
    print("=" * 80)
    print("🗑️  DELETING .keep FILES")
    print("=" * 80)

    # Get all resources
    result = cloudinary.api.resources(
        type='upload',
        prefix='Shyam/Finest Coating Shyam',
        max_results=500
    )

    keep_files = []
    for img in result['resources']:
        if img['public_id'].endswith('.keep'):
            keep_files.append(img['public_id'])

    print(f"\n📋 Found {len(keep_files)} .keep files to delete\n")

    deleted = 0
    for public_id in keep_files:
        try:
            cloudinary.uploader.destroy(public_id)
            print(f"✅ Deleted: {public_id}")
            deleted += 1
        except Exception as e:
            print(f"❌ Failed: {public_id} - {str(e)}")

    print("\n" + "=" * 80)
    print(f"✅ Deleted {deleted} .keep files")
    print("=" * 80)
    print("\n🔄 Now refresh Cloudinary console - actual images should appear!\n")

if __name__ == "__main__":
    main()
