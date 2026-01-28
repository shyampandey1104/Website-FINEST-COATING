import json
import re

# Load Cloudinary URLs
with open('/Users/shyamkumarpandey/html/cloudinary_urls.json', 'r') as f:
    urls = json.load(f)

# Read HTML file
with open('/Users/shyamkumarpandey/html/blue_color_website.html', 'r') as f:
    html = f.read()

# Create mapping of old paths to new URLs
replacements = {
    # Bathtub
    'src="images/bathtub/bathtub-refinishing.png"': f'src="{urls["bathtub"]["bathtub-refinishing.png"]}"',

    # Urinals
    'src="images/urinals/How-To-Keep-Urinals-Clean.jpg"': f'src="{urls["urinals"]["How-To-Keep-Urinals-Clean.jpg"]}"',

    # Kitchen
    'src="images/kitchen/Gemini_Generated_Image_ggp5esggp5esggp5.png"': f'src="{urls["kitchen"]["Gemini_Generated_Image_ggp5esggp5esggp5.png"]}"',

    # Decorative
    'src="images/decorative/decorative-items.jpeg"': f'src="{urls["decorative"]["decorative-items.jpeg"]}"',
}

# Industrial images
for filename, url in urls.get("industrial", {}).items():
    old_path = f'src="images/industrial/{filename}"'
    new_path = f'src="{url}"'
    replacements[old_path] = new_path

# Apply replacements
for old, new in replacements.items():
    html = html.replace(old, new)

# Also handle the hero image
html = html.replace('src="images/hero_bathtub.png"', f'src="{urls["root"]["hero_bathtub.png"]}"')

# Save updated HTML
with open('/Users/shyamkumarpandey/html/blue_color_website.html', 'w') as f:
    f.write(html)

print("✅ HTML file updated with Cloudinary URLs!")
