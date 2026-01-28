import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import glob

# Cloudinary configuration
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

# Define source folder and images
downloads_folder = "/Users/shyamkumarpandey/Downloads"
cloudinary_folder = "Finest Coating/Before After Transformations"

# List of images to upload
image_files = [
    "WhatsApp Image 2026-01-12 at 9.19.31 PM.jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.31 PM (2).jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.31 PM (1).jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.30 PM.jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.30 PM (3).jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.30 PM (2).jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.30 PM (1).jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.28 PM (4).jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.28 PM (2).jpeg",
    "WhatsApp Image 2026-01-12 at 9.19.27 PM (1).jpeg",
]

uploaded_urls = []

print("Starting upload to Cloudinary...")
print(f"Target folder: {cloudinary_folder}")
print("-" * 50)

for i, image_name in enumerate(image_files, 1):
    image_path = os.path.join(downloads_folder, image_name)

    if not os.path.exists(image_path):
        print(f"[{i}] ERROR: File not found - {image_name}")
        continue

    # Create a clean public_id from the filename
    public_id = f"transformation_{i}"

    try:
        print(f"[{i}] Uploading: {image_name}...")

        result = cloudinary.uploader.upload(
            image_path,
            folder=cloudinary_folder,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )

        url = result['secure_url']
        uploaded_urls.append(url)
        print(f"    SUCCESS: {url}")

    except Exception as e:
        print(f"    ERROR: {str(e)}")

print("-" * 50)
print(f"\nUpload Complete! {len(uploaded_urls)} images uploaded.")
print("\nUploaded URLs:")
for i, url in enumerate(uploaded_urls, 1):
    print(f"{i}. {url}")
