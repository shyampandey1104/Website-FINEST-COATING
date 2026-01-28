#!/usr/bin/env python3
"""
Delete ALL images from Shyam folder in Cloudinary
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
print("🗑️  Delete ALL Shyam Images from Cloudinary")
print("=" * 60)

total_deleted = 0

# Delete all images with prefix "Shyam"
print("\n🗑️  Deleting all images with prefix 'Shyam'...")

try:
    # Keep deleting until no more images
    while True:
        # Get resources
        result = cloudinary.api.resources(
            type="upload",
            prefix="Shyam",
            max_results=100
        )

        resources = result.get('resources', [])
        if not resources:
            break

        # Get public_ids
        public_ids = [r['public_id'] for r in resources]

        # Delete them
        delete_result = cloudinary.api.delete_resources(public_ids)

        deleted = len([k for k, v in delete_result.get('deleted', {}).items() if v == 'deleted'])
        total_deleted += deleted
        print(f"   ✅ Deleted batch of {deleted} images... (Total: {total_deleted})")

except Exception as e:
    print(f"   ⚠️  Error: {str(e)}")

# Now delete all folders under Shyam
print("\n🗑️  Deleting all Shyam folders...")

folders_to_delete = [
    "Shyam/Finest_Coating/blue_color_website/bathroom",
    "Shyam/Finest_Coating/blue_color_website/bathtub",
    "Shyam/Finest_Coating/blue_color_website/decorative",
    "Shyam/Finest_Coating/blue_color_website/industrial",
    "Shyam/Finest_Coating/blue_color_website/kitchen",
    "Shyam/Finest_Coating/blue_color_website/services",
    "Shyam/Finest_Coating/blue_color_website/urinals",
    "Shyam/Finest_Coating/blue_color_website",
    "Shyam/Finest_Coating",
    "Shyam/Finest Coating Shyam/Gallery/Before After",
    "Shyam/Finest Coating Shyam/Gallery",
    "Shyam/Finest Coating Shyam/General",
    "Shyam/Finest Coating Shyam/Industries/Ducting Pump Room",
    "Shyam/Finest Coating Shyam/Industries/Health Care",
    "Shyam/Finest Coating Shyam/Industries/Hotels Resorts",
    "Shyam/Finest Coating Shyam/Industries/Industrial Machinery",
    "Shyam/Finest Coating Shyam/Industries/Medical Machineries",
    "Shyam/Finest Coating Shyam/Industries/Multi-Surface Coating",
    "Shyam/Finest Coating Shyam/Industries/Ships Yachts Parts",
    "Shyam/Finest Coating Shyam/Industries/Waterslides FRP",
    "Shyam/Finest Coating Shyam/Industries",
    "Shyam/Finest Coating Shyam/Services",
    "Shyam/Finest Coating Shyam/Warranty",
    "Shyam/Finest Coating Shyam",
    "Shyam"
]

for folder in folders_to_delete:
    try:
        cloudinary.api.delete_folder(folder)
        print(f"   ✅ Deleted folder: {folder}")
    except Exception as e:
        pass

print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print(f"   🗑️  Total images deleted: {total_deleted}")
print("=" * 60)
print("\n✅ Done! All Shyam folder images have been deleted from Cloudinary.")
