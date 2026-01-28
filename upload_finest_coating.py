#!/usr/bin/env python3
"""
Upload all images to Cloudinary under Finest Coating folder
Section-wise folders banayenge
"""

import cloudinary
import cloudinary.uploader
import os
import json
from pathlib import Path

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

# Base paths
BASE_PATH = "/Users/shyamkumarpandey/html"
IMAGES_PATH = "/Users/shyamkumarpandey/html/images"

# Main Cloudinary folder
MAIN_FOLDER = "Finest Coating"

# Image extensions
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')

# Store all uploaded URLs
uploaded_urls = {}

def upload_image(file_path, folder):
    """Upload single image to Cloudinary"""
    try:
        file_name = Path(file_path).stem

        result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            public_id=file_name,
            overwrite=True,
            resource_type="image"
        )

        return result.get('secure_url')
    except Exception as e:
        print(f"   ❌ Error uploading {file_path}: {str(e)}")
        return None

def upload_folder(folder_path, cloudinary_folder, folder_name):
    """Upload all images from a folder"""
    if not os.path.exists(folder_path):
        print(f"   ⚠️  Folder not found: {folder_path}")
        return 0

    count = 0
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(IMAGE_EXTENSIONS)]

    if not files:
        print(f"   ⚠️  No images in {folder_name}")
        return 0

    print(f"\n📁 {folder_name.upper()} ({len(files)} images)")
    print("-" * 40)

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            url = upload_image(file_path, cloudinary_folder)
            if url:
                print(f"   ✅ {filename}")
                uploaded_urls[f"{folder_name}/{filename}"] = url
                count += 1
            else:
                print(f"   ❌ {filename}")

    return count

print("=" * 60)
print("🚀 Cloudinary Upload - Finest Coating")
print("=" * 60)
print(f"📁 Main Folder: {MAIN_FOLDER}")

total_uploaded = 0

# 1. HERO Section
print("\n" + "=" * 60)
print("📷 HERO SECTION")
print("=" * 60)
hero_images = ['hero-bathtub.png', 'hero_bathtub.png']
for img in hero_images:
    path = os.path.join(BASE_PATH, img)
    if os.path.exists(path):
        url = upload_image(path, f"{MAIN_FOLDER}/Hero")
        if url:
            print(f"   ✅ {img}")
            uploaded_urls[f"hero/{img}"] = url
            total_uploaded += 1
    path = os.path.join(IMAGES_PATH, img)
    if os.path.exists(path):
        url = upload_image(path, f"{MAIN_FOLDER}/Hero")
        if url:
            print(f"   ✅ {img}")
            uploaded_urls[f"hero/{img}"] = url
            total_uploaded += 1

# 2. BATHTUB Section (Before/After)
print("\n" + "=" * 60)
print("📷 BATHTUB SECTION (Before/After)")
print("=" * 60)

# Before images
before_images = [f for f in os.listdir(BASE_PATH) if f.startswith('bathtub-before') and f.lower().endswith(IMAGE_EXTENSIONS)]
print(f"\n📁 BEFORE ({len(before_images)} images)")
for img in sorted(before_images):
    path = os.path.join(BASE_PATH, img)
    url = upload_image(path, f"{MAIN_FOLDER}/Bathtub/Before")
    if url:
        print(f"   ✅ {img}")
        uploaded_urls[f"bathtub/before/{img}"] = url
        total_uploaded += 1

# After images
after_images = [f for f in os.listdir(BASE_PATH) if f.startswith('bathtub-after') and f.lower().endswith(IMAGE_EXTENSIONS)]
print(f"\n📁 AFTER ({len(after_images)} images)")
for img in sorted(after_images):
    path = os.path.join(BASE_PATH, img)
    url = upload_image(path, f"{MAIN_FOLDER}/Bathtub/After")
    if url:
        print(f"   ✅ {img}")
        uploaded_urls[f"bathtub/after/{img}"] = url
        total_uploaded += 1

# Bathtub folder images
count = upload_folder(
    os.path.join(IMAGES_PATH, "bathtub"),
    f"{MAIN_FOLDER}/Bathtub/Gallery",
    "bathtub"
)
total_uploaded += count

# 3. BATHROOM Section
print("\n" + "=" * 60)
print("📷 BATHROOM SECTION")
print("=" * 60)
count = upload_folder(
    os.path.join(IMAGES_PATH, "bathroom"),
    f"{MAIN_FOLDER}/Bathroom",
    "bathroom"
)
total_uploaded += count

# 4. URINALS Section
print("\n" + "=" * 60)
print("📷 URINALS SECTION")
print("=" * 60)

# Root urinal images
urinal_images = ['How-To-Keep-Urinals-Clean.jpg', 'download.jpeg', 'download1.jpeg',
                 'download2.jpeg', 'download3.jpeg', 'images.jpeg']
print(f"\n📁 URINALS ({len(urinal_images)} images)")
for img in urinal_images:
    path = os.path.join(BASE_PATH, img)
    if os.path.exists(path):
        url = upload_image(path, f"{MAIN_FOLDER}/Urinals")
        if url:
            print(f"   ✅ {img}")
            uploaded_urls[f"urinals/{img}"] = url
            total_uploaded += 1

# Urinals folder
count = upload_folder(
    os.path.join(IMAGES_PATH, "urinals"),
    f"{MAIN_FOLDER}/Urinals",
    "urinals_folder"
)
total_uploaded += count

# 5. KITCHEN Section
print("\n" + "=" * 60)
print("📷 KITCHEN SECTION")
print("=" * 60)

# Root kitchen images
kitchen_images = [f for f in os.listdir(BASE_PATH) if f.startswith('kitchen') and f.lower().endswith(IMAGE_EXTENSIONS)]
print(f"\n📁 KITCHEN ({len(kitchen_images)} images)")
for img in sorted(kitchen_images):
    path = os.path.join(BASE_PATH, img)
    url = upload_image(path, f"{MAIN_FOLDER}/Kitchen")
    if url:
        print(f"   ✅ {img}")
        uploaded_urls[f"kitchen/{img}"] = url
        total_uploaded += 1

# Kitchen folder
count = upload_folder(
    os.path.join(IMAGES_PATH, "kitchen"),
    f"{MAIN_FOLDER}/Kitchen",
    "kitchen_folder"
)
total_uploaded += count

# 6. BUFFING & POLISHING Section
print("\n" + "=" * 60)
print("📷 BUFFING & POLISHING SECTION")
print("=" * 60)

buffing_images = [f for f in os.listdir(BASE_PATH) if f.startswith('buffing') and f.lower().endswith(IMAGE_EXTENSIONS)]
print(f"\n📁 BUFFING ({len(buffing_images)} images)")
for img in sorted(buffing_images):
    path = os.path.join(BASE_PATH, img)
    url = upload_image(path, f"{MAIN_FOLDER}/Buffing")
    if url:
        print(f"   ✅ {img}")
        uploaded_urls[f"buffing/{img}"] = url
        total_uploaded += 1

# 7. DECORATIVE Section
print("\n" + "=" * 60)
print("📷 DECORATIVE SECTION")
print("=" * 60)
count = upload_folder(
    os.path.join(IMAGES_PATH, "decorative"),
    f"{MAIN_FOLDER}/Decorative",
    "decorative"
)
total_uploaded += count

# 8. INDUSTRIAL Section
print("\n" + "=" * 60)
print("📷 INDUSTRIAL SECTION")
print("=" * 60)
count = upload_folder(
    os.path.join(IMAGES_PATH, "industrial"),
    f"{MAIN_FOLDER}/Industrial",
    "industrial"
)
total_uploaded += count

# 9. SERVICES Section
print("\n" + "=" * 60)
print("📷 SERVICES SECTION")
print("=" * 60)
count = upload_folder(
    os.path.join(IMAGES_PATH, "services"),
    f"{MAIN_FOLDER}/Services",
    "services"
)
total_uploaded += count

# 10. OTHER Images (Benefits, FAQ, etc.)
print("\n" + "=" * 60)
print("📷 OTHER IMAGES")
print("=" * 60)

other_images = ['benefits-image-2.jpeg', 'faq-image-2.jpeg']
for img in other_images:
    path = os.path.join(BASE_PATH, img)
    if os.path.exists(path):
        url = upload_image(path, f"{MAIN_FOLDER}/Other")
        if url:
            print(f"   ✅ {img}")
            uploaded_urls[f"other/{img}"] = url
            total_uploaded += 1

# 11. LOGO Section
print("\n" + "=" * 60)
print("📷 LOGO SECTION")
print("=" * 60)
count = upload_folder(
    os.path.join(IMAGES_PATH, "logo"),
    f"{MAIN_FOLDER}/Logo",
    "logo"
)
total_uploaded += count

# Save URLs to JSON
json_file = os.path.join(BASE_PATH, "finest_coating_urls.json")
with open(json_file, 'w') as f:
    json.dump(uploaded_urls, f, indent=2)

# Final Summary
print("\n" + "=" * 60)
print("📊 FINAL SUMMARY")
print("=" * 60)
print(f"   ✅ Total images uploaded: {total_uploaded}")
print(f"   📁 Main folder: {MAIN_FOLDER}")
print(f"   💾 URLs saved to: {json_file}")
print("\n📂 Folder Structure:")
print(f"   {MAIN_FOLDER}/")
print("   ├── Hero/")
print("   ├── Bathtub/")
print("   │   ├── Before/")
print("   │   ├── After/")
print("   │   └── Gallery/")
print("   ├── Bathroom/")
print("   ├── Urinals/")
print("   ├── Kitchen/")
print("   ├── Buffing/")
print("   ├── Decorative/")
print("   ├── Industrial/")
print("   ├── Services/")
print("   ├── Other/")
print("   └── Logo/")
print("=" * 60)
print("\n🎉 All images uploaded to Cloudinary successfully!")
