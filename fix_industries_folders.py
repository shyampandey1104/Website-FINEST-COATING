import cloudinary
import cloudinary.uploader
import requests
import os
import tempfile

# Configure Cloudinary
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg"
)

# HTML file path
html_file = "/Users/shyamkumarpandey/html/blue_color_website.html"

# Read HTML file
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Industries We Serve images - matching your Cloudinary folder structure exactly
industries_images = [
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646772/Abdul%20Images/Finest%20Coating/Industries%20We%20Serve/Ships%20and%20Yachts/ships_yachts.jpg",
        "folder": "Ships Yachts Parts",
        "name": "ships_yachts_main"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646774/Abdul%20Images/Finest%20Coating/Industries%20We%20Serve/Medical%20Machineries/medical_equipment.png",
        "folder": "Medical Machineries",
        "name": "medical_equipment_main"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646775/Abdul%20Images/Finest%20Coating/Industries%20We%20Serve/Industrial%20Machinery/industrial_machinery.jpg",
        "folder": "Industrial Machinery",
        "name": "industrial_machinery_main"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646776/Abdul%20Images/Finest%20Coating/Industries%20We%20Serve/Ducting%20Pump%20Room/ducting_pump_room.jpg",
        "folder": "Ducting Pump Room",
        "name": "ducting_pump_room_main"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646777/Abdul%20Images/Finest%20Coating/Industries%20We%20Serve/Waterslides%20FRP/waterslides.jpg",
        "folder": "Waterslides FRP",
        "name": "waterslides_main"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646779/Abdul%20Images/Finest%20Coating/Industries%20We%20Serve/Multi%20Surface%20Coating/multi_surface.jpg",
        "folder": "Multi-Surface Coating",
        "name": "multi_surface_main"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646780/Abdul%20Images/Finest%20Coating/Industries%20We%20Serve/Hotels%20and%20Resorts/hotels_resorts.jpg",
        "folder": "Hotels Resorts",
        "name": "hotels_resorts_main"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646781/Abdul%20Images/Finest%20Coating/Industries%20We%20Serve/Health%20Care/healthcare.jpg",
        "folder": "Health Care",
        "name": "healthcare_main"
    }
]

print("=" * 60)
print("Uploading Images to Industries We Serve Subfolders")
print("=" * 60)

url_mapping = {}
success_count = 0

for i, img in enumerate(industries_images, 1):
    try:
        print(f"\n[{i}/{len(industries_images)}] Processing: {img['folder']}")

        # Download image from current URL
        print(f"  Downloading...")
        response = requests.get(img['current_url'], timeout=30)

        if response.status_code != 200:
            print(f"  Failed to download: HTTP {response.status_code}")
            continue

        # Determine file extension
        content_type = response.headers.get('content-type', '')
        if 'png' in content_type:
            ext = 'png'
        elif 'webp' in content_type:
            ext = 'webp'
        else:
            ext = 'jpg'

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        # Upload with exact folder structure matching Cloudinary
        # Format: Abdul Images/Finest Coating/Industries We Serve/[Folder Name]/[filename]
        public_id = f"Abdul Images/Finest Coating/Industries We Serve/{img['folder']}/{img['name']}"

        print(f"  Uploading to: Industries We Serve/{img['folder']}/")

        result = cloudinary.uploader.upload(
            tmp_path,
            public_id=public_id,
            overwrite=True,
            resource_type="image",
            folder=""  # Don't add extra folder prefix
        )

        new_url = result['secure_url']
        url_mapping[img['current_url']] = new_url
        success_count += 1

        print(f"  ✅ Done!")
        print(f"  URL: {new_url}")

        # Clean up temp file
        os.unlink(tmp_path)

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

# Update HTML file
print(f"\n{'=' * 60}")
print(f"Updating HTML file with {len(url_mapping)} new URLs...")
print("=" * 60)

updated_html = html_content
for old_url, new_url in url_mapping.items():
    updated_html = updated_html.replace(old_url, new_url)

# Write updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print(f"\n{'=' * 60}")
print(f"COMPLETE!")
print("=" * 60)
print(f"Successfully uploaded: {success_count}/{len(industries_images)} images")
print(f"\n🔄 Now refresh your Cloudinary console to see images in folders!")
