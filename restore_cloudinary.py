#!/usr/bin/env python3
"""
Check if deleted images can be restored from Cloudinary
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
print("🔄 Checking Cloudinary for Deleted Images")
print("=" * 60)

# Try to list deleted resources
try:
    print("\n📋 Checking for deleted resources...")

    # Check if there are any resources that can be restored
    result = cloudinary.api.resources(
        type="upload",
        max_results=500
    )

    current_count = len(result.get('resources', []))
    print(f"   Current images in account: {current_count}")

    # Try to access backup/deleted resources
    # Cloudinary has a "Backup" feature but it needs to be enabled
    print("\n⚠️  Cloudinary mein deleted images ko restore karne ke liye:")
    print("   1. Cloudinary Console mein jaao")
    print("   2. Settings > Upload > Backup & Restore")
    print("   3. Agar Backup enabled hai to deleted images restore ho sakti hain")
    print("   4. Ya phir 'Deleted Assets' section check karo")

except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("📌 SOLUTION:")
print("=" * 60)
print("""
1. Cloudinary Console mein jaao:
   https://console.cloudinary.com/

2. Left menu mein 'Media Library' click karo

3. Top right mein 'Trash' ya 'Deleted' icon dekhao
   - Agar hai to wahan se restore kar sakte ho

4. Ya Settings > Upload Settings > Backup check karo

5. Agar backup enabled nahi tha, to images permanently
   delete ho gayi hain aur recover nahi ho sakti
""")
