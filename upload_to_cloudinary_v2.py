import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import json

# Configure Cloudinary
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

# Base path
base_path = "/Users/shyamkumarpandey/html/images"

# Store uploaded URLs
uploaded_urls = {}

def upload_image(file_path, folder_path):
    """Upload a single image to Cloudinary with proper folder structure"""
    try:
        filename = os.path.basename(file_path)
        # Clean filename for public_id (remove special chars)
        clean_name = os.path.splitext(filename)[0]
        public_id = f"{folder_path}/{clean_name}"

        result = cloudinary.uploader.upload(
            file_path,
            public_id=public_id,
            overwrite=True,
            resource_type="image",
            folder=""  # folder is included in public_id
        )
        print(f"✅ {filename}")
        return result['secure_url']
    except Exception as e:
        print(f"❌ {file_path} - {str(e)}")
        return None

def upload_folder(local_folder, cloudinary_folder):
    """Upload all images from a local folder to Cloudinary folder"""
    if not os.path.exists(local_folder):
        print(f"⚠️ Folder not found: {local_folder}")
        return {}

    folder_urls = {}
    files = [f for f in os.listdir(local_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]

    print(f"\n📁 {cloudinary_folder}/ ({len(files)} files)")

    for filename in files:
        file_path = os.path.join(local_folder, filename)
        url = upload_image(file_path, cloudinary_folder)
        if url:
            folder_urls[filename] = url

    return folder_urls

print("🚀 Uploading to Cloudinary...")
print("📂 Structure: Finest Coating/[subfolders]/[images]\n")

# Main folder structure: Finest Coating/subfolder/images
main_folder = "Finest Coating"

# Upload each subfolder
subfolders = ['bathtub', 'urinals', 'kitchen', 'decorative', 'bathroom', 'services', 'industrial']

for subfolder in subfolders:
    local_path = os.path.join(base_path, subfolder)
    cloudinary_path = f"{main_folder}/{subfolder}"
    uploaded_urls[subfolder] = upload_folder(local_path, cloudinary_path)

# Upload root level images to main folder
print(f"\n📁 {main_folder}/ (root images)")
root_files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
uploaded_urls["root"] = {}
for filename in root_files:
    file_path = os.path.join(base_path, filename)
    url = upload_image(file_path, main_folder)
    if url:
        uploaded_urls["root"][filename] = url

# Save URLs
with open('/Users/shyamkumarpandey/html/cloudinary_urls_v2.json', 'w') as f:
    json.dump(uploaded_urls, f, indent=2)

print("\n" + "="*50)
print("✅ All done!")
print("="*50)
print(f"\n📂 Cloudinary Structure:")
print(f"   Finest Coating/")
for folder in subfolders:
    count = len(uploaded_urls.get(folder, {}))
    if count > 0:
        print(f"   ├── {folder}/ ({count} images)")
print(f"   └── (root images: {len(uploaded_urls.get('root', {}))})")
print(f"\n📄 URLs saved to: cloudinary_urls_v2.json")
