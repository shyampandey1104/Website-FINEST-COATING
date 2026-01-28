#!/usr/bin/env python3
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

# Upload image
image_path = "/Users/shyamkumarpandey/Downloads/mumbai-bathroom.jpg"
folder_name = "Finest Coating/Mumbai's Most Trusted Bathroom Re-glazing Experts"

print("Uploading image to Cloudinary...")

result = cloudinary.uploader.upload(
    image_path,
    folder=folder_name,
    public_id="mumbai-bathroom",
    overwrite=True,
    resource_type="image"
)

print(f"\n✅ Upload successful!")
print(f"URL: {result.get('secure_url')}")
