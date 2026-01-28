import cloudinary
import cloudinary.uploader
import os
import json

# Configure Cloudinary
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

base_path = "/Users/shyamkumarpandey/html/images"
uploaded_urls = {}

def upload_image(file_path, folder):
    try:
        filename = os.path.basename(file_path)
        result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            overwrite=True,
            resource_type="image"
        )
        print(f"✅ {filename}")
        return result['secure_url']
    except Exception as e:
        print(f"❌ {filename} - {str(e)}")
        return None

# Main folder in Abdul Images
main_folder = "Abdul Images/Finest Coating"

subfolders = ['bathtub', 'urinals', 'kitchen', 'decorative', 'bathroom', 'services', 'industrial']

print("🚀 Uploading to: Abdul Images/Finest Coating/\n")

for subfolder in subfolders:
    local_path = os.path.join(base_path, subfolder)
    if not os.path.exists(local_path):
        continue

    cloud_folder = f"{main_folder}/{subfolder}"
    files = [f for f in os.listdir(local_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]

    if not files:
        continue

    print(f"\n📁 {subfolder}/ ({len(files)} files)")
    uploaded_urls[subfolder] = {}

    for filename in files:
        file_path = os.path.join(local_path, filename)
        url = upload_image(file_path, cloud_folder)
        if url:
            uploaded_urls[subfolder][filename] = url

# Root images
print(f"\n📁 Root images")
uploaded_urls["root"] = {}
for filename in os.listdir(base_path):
    file_path = os.path.join(base_path, filename)
    if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
        url = upload_image(file_path, main_folder)
        if url:
            uploaded_urls["root"][filename] = url

with open('/Users/shyamkumarpandey/html/cloudinary_final_urls.json', 'w') as f:
    json.dump(uploaded_urls, f, indent=2)

print("\n✅ Done! Check Cloudinary: Abdul Images > Finest Coating")
