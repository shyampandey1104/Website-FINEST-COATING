import cloudinary
import cloudinary.uploader
import re
import os

# Configure Cloudinary
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

# Paths
html_file = "/Users/shyamkumarpandey/html/blue_color_website.html"
base_path = "/Users/shyamkumarpandey/html"

# Read HTML file
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find all local image paths (images/...)
local_pattern = r'src="(images/[^"]+)"'
local_images = list(set(re.findall(local_pattern, html_content)))

print(f"Found {len(local_images)} unique local images to upload\n")

# Upload each image to Cloudinary with proper folder structure
url_mapping = {}
success_count = 0
fail_count = 0

for i, img_path in enumerate(local_images, 1):
    full_path = os.path.join(base_path, img_path)

    # Check if file exists
    if not os.path.exists(full_path):
        print(f"[{i}/{len(local_images)}] ❌ File not found: {img_path}")
        fail_count += 1
        continue

    try:
        # Get folder structure from path (e.g., images/bathroom -> bathroom)
        path_parts = img_path.split('/')
        if len(path_parts) >= 2:
            folder_name = path_parts[1]  # bathroom, industrial, services, etc.
        else:
            folder_name = "misc"

        # Get filename without extension for public_id
        filename = os.path.basename(img_path)
        name_without_ext = os.path.splitext(filename)[0]

        # Create public_id with folder structure
        public_id = f"Abdul Images/Finest Coating/{folder_name}/{name_without_ext}"

        print(f"[{i}/{len(local_images)}] Uploading {filename} to {folder_name}/...")

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            full_path,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )

        cloudinary_url = result['secure_url']
        url_mapping[img_path] = cloudinary_url
        success_count += 1
        print(f"  ✅ Done: {cloudinary_url[:80]}...")

    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        fail_count += 1

# Replace URLs in HTML
print(f"\n📝 Updating HTML file with {len(url_mapping)} new URLs...")
updated_html = html_content

for old_path, new_url in url_mapping.items():
    # Replace src="images/..." with src="cloudinary_url"
    updated_html = updated_html.replace(f'src="{old_path}"', f'src="{new_url}"')

# Write updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print(f"\n{'='*50}")
print(f"✅ Upload Complete!")
print(f"{'='*50}")
print(f"Total images found: {len(local_images)}")
print(f"Successfully uploaded: {success_count}")
print(f"Failed: {fail_count}")
print(f"\nHTML file updated with Cloudinary URLs!")
print(f"\nCloudinary Folder Structure:")
print(f"📂 Abdul Images/")
print(f"└── 📁 Finest Coating/")
print(f"    ├── 📂 bathroom/")
print(f"    ├── 📂 industrial/")
print(f"    ├── 📂 services/")
print(f"    ├── 📂 bathtub/")
print(f"    ├── 📂 urinals/")
print(f"    ├── 📂 kitchen/")
print(f"    └── 📂 decorative/")
