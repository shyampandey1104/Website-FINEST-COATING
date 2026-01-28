import cloudinary
import cloudinary.uploader
import requests
import re
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

# Industries We Serve section images with their proper folder names
industries_images = [
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767645927/Abdul%20Images/Finest%20Coating/industries/1567899378494.jpg",
        "folder": "Ships and Yachts",
        "name": "ships_yachts"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767646206/Abdul%20Images/Finest%20Coating/industrial/1765746870906.png",
        "folder": "Medical Machineries",
        "name": "medical_equipment"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767645909/Abdul%20Images/Finest%20Coating/industries/1581091226825.jpg",
        "folder": "Industrial Machinery",
        "name": "industrial_machinery"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767645910/Abdul%20Images/Finest%20Coating/industries/1504328345606.jpg",
        "folder": "Ducting Pump Room",
        "name": "ducting_pump_room"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767645905/Abdul%20Images/Finest%20Coating/industries/1558979158.jpg",
        "folder": "Waterslides FRP",
        "name": "waterslides"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767645908/Abdul%20Images/Finest%20Coating/industries/1558618666.jpg",
        "folder": "Multi Surface Coating",
        "name": "multi_surface"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767645931/Abdul%20Images/Finest%20Coating/industries/1566073771259.jpg",
        "folder": "Hotels and Resorts",
        "name": "hotels_resorts"
    },
    {
        "current_url": "https://res.cloudinary.com/dd2sbrcrr/image/upload/v1767645915/Abdul%20Images/Finest%20Coating/industries/1516549655169.jpg",
        "folder": "Health Care",
        "name": "healthcare"
    }
]

print("=" * 60)
print("Re-organizing Industries We Serve Images")
print("=" * 60)

url_mapping = {}
success_count = 0

for i, img in enumerate(industries_images, 1):
    try:
        print(f"\n[{i}/{len(industries_images)}] Processing: {img['folder']}")

        # Download image from current URL
        print(f"  Downloading from current location...")
        response = requests.get(img['current_url'], timeout=30)

        if response.status_code != 200:
            print(f"  Failed to download: HTTP {response.status_code}")
            continue

        # Save to temp file
        ext = img['current_url'].split('.')[-1].split('?')[0]
        with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        # Upload to new location
        public_id = f"Abdul Images/Finest Coating/Industries We Serve/{img['folder']}/{img['name']}"

        print(f"  Uploading to: Industries We Serve/{img['folder']}/")

        result = cloudinary.uploader.upload(
            tmp_path,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )

        new_url = result['secure_url']
        url_mapping[img['current_url']] = new_url
        success_count += 1

        print(f"  Done: {new_url[:70]}...")

        # Clean up temp file
        os.unlink(tmp_path)

    except Exception as e:
        print(f"  Error: {str(e)}")

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
print(f"Successfully re-organized: {success_count}/{len(industries_images)} images")
print(f"\nNew Cloudinary Folder Structure:")
print(f"Abdul Images/")
print(f"└── Finest Coating/")
print(f"    └── Industries We Serve/")
for img in industries_images:
    print(f"        ├── {img['folder']}/")
