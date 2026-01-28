import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

# Folder name in Cloudinary
FOLDER_NAME = "bathtubs_washbasins"

# Images to upload
images_to_upload = [
    "/Users/shyamkumarpandey/Downloads/bartub_images.jpg",
    "/Users/shyamkumarpandey/Downloads/download.jpeg",
    "/Users/shyamkumarpandey/Downloads/WhatsApp Image 2026-01-12 at 9.19.28 PM (1).jpeg",
    "/Users/shyamkumarpandey/Downloads/WhatsApp Image 2026-01-12 at 9.19.28 PM (2).jpeg",
    "/Users/shyamkumarpandey/Downloads/WhatsApp Image 2026-01-12 at 9.19.28 PM (3).jpeg",
    "/Users/shyamkumarpandey/Downloads/WhatsApp Image 2026-01-12 at 9.19.27 PM.jpeg",
    "/Users/shyamkumarpandey/Downloads/WhatsApp Image 2026-01-12 at 9.19.27 PM (1).jpeg",
    "/Users/shyamkumarpandey/Downloads/WhatsApp Image 2026-01-12 at 9.19.27 PM (2).jpeg",
    "/Users/shyamkumarpandey/Downloads/WhatsApp Image 2026-01-12 at 9.19.27 PM (3).jpeg",
]

def upload_images():
    print(f"Uploading images to folder: {FOLDER_NAME}")
    print("=" * 50)

    uploaded_urls = []

    for image_path in images_to_upload:
        if os.path.exists(image_path):
            try:
                # Get filename without extension for public_id
                filename = os.path.splitext(os.path.basename(image_path))[0]
                # Clean filename for Cloudinary
                clean_name = filename.replace(" ", "_").replace("(", "").replace(")", "")

                print(f"\nUploading: {os.path.basename(image_path)}")

                # Upload to Cloudinary with folder
                result = cloudinary.uploader.upload(
                    image_path,
                    folder=FOLDER_NAME,
                    public_id=clean_name,
                    overwrite=True
                )

                print(f"  ✓ Success!")
                print(f"  URL: {result['secure_url']}")
                uploaded_urls.append(result['secure_url'])

            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
        else:
            print(f"\n✗ File not found: {image_path}")

    print("\n" + "=" * 50)
    print(f"Total uploaded: {len(uploaded_urls)} images")
    print("\nAll URLs:")
    for url in uploaded_urls:
        print(url)

if __name__ == "__main__":
    upload_images()
