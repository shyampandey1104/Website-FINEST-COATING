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

# Find all Unsplash image URLs
unsplash_pattern = r'https://images\.unsplash\.com/[^"\s)>]+'
unsplash_urls = list(set(re.findall(unsplash_pattern, html_content)))

print(f"Found {len(unsplash_urls)} unique Unsplash images to upload\n")

# Upload each image to Cloudinary
url_mapping = {}

for i, url in enumerate(unsplash_urls, 1):
    try:
        # Extract photo ID from URL for naming
        photo_id_match = re.search(r'photo-(\d+)', url)
        if photo_id_match:
            photo_id = photo_id_match.group(1)
        else:
            photo_id = f"unsplash_{i}"

        public_id = f"Abdul Images/Finest Coating/industries/{photo_id}"

        print(f"[{i}/{len(unsplash_urls)}] Uploading {photo_id}...")

        # Upload directly from URL to Cloudinary
        result = cloudinary.uploader.upload(
            url,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )

        cloudinary_url = result['secure_url']
        url_mapping[url] = cloudinary_url
        print(f"  ✅ Done: {cloudinary_url}")

    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")

# Replace URLs in HTML
print("\n📝 Updating HTML file...")
updated_html = html_content

for old_url, new_url in url_mapping.items():
    updated_html = updated_html.replace(old_url, new_url)

# Write updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print(f"\n✅ Done! Updated {len(url_mapping)} images in HTML file")
print(f"❌ Failed: {len(unsplash_urls) - len(url_mapping)} images")
