#!/usr/bin/env python3
"""
Test upload to force folder creation in Cloudinary console
"""

import cloudinary
import cloudinary.uploader
import io
from PIL import Image

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg",
    secure=True
)

def create_test_image():
    """Create a simple test image"""
    # Create a 100x100 red image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def main():
    print("=" * 80)
    print("🧪 TEST UPLOAD TO SHYAM/FINEST COATING SHYAM")
    print("=" * 80)

    # Create test image
    print("\n📸 Creating test image...")
    test_image = create_test_image()

    # Upload to Shyam/Finest Coating Shyam
    folder = "Shyam/Finest Coating Shyam"
    public_id = f"{folder}/test_image"

    print(f"\n⬆️  Uploading to: {folder}/")

    try:
        result = cloudinary.uploader.upload(
            test_image,
            public_id=public_id,
            folder=folder,
            overwrite=True,
            resource_type="image"
        )

        print(f"✅ Success!")
        print(f"\nCloudinary URL: {result['secure_url']}")
        print(f"Public ID: {result['public_id']}")

        print("\n" + "=" * 80)
        print("✨ Now check Cloudinary console - 'Shyam' folder should appear!")
        print("=" * 80)

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
