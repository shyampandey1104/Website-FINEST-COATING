#!/usr/bin/env python3
"""
Verify that Shyam folder exists on Cloudinary and list all folders
"""

import cloudinary
import cloudinary.api

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dd2sbrcrr",
    api_key="173777767114771",
    api_secret="vcbZWirynnzsfWAlOgg-Jg6Xyqg",
    secure=True
)

def list_folders(prefix=""):
    """List all folders in Cloudinary"""
    try:
        result = cloudinary.api.root_folders()
        print("\n📁 Root Folders in Cloudinary:")
        print("=" * 80)
        for folder in result['folders']:
            print(f"   • {folder['name']} ({folder.get('path', 'N/A')})")
        print("=" * 80)
        return result
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def list_subfolders(folder_path):
    """List subfolders in a specific folder"""
    try:
        result = cloudinary.api.subfolders(folder_path)
        print(f"\n📂 Subfolders in '{folder_path}':")
        print("=" * 80)
        for folder in result['folders']:
            print(f"   • {folder['name']} ({folder.get('path', 'N/A')})")
        print("=" * 80)
        return result
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def list_resources_in_folder(folder_path, max_results=10):
    """List images in a specific folder"""
    try:
        result = cloudinary.api.resources(
            type="upload",
            prefix=folder_path,
            max_results=max_results
        )
        print(f"\n🖼️  Images in '{folder_path}' (showing first {max_results}):")
        print("=" * 80)
        for resource in result['resources']:
            print(f"   • {resource['public_id']}")
            print(f"     URL: {resource['secure_url']}")
        print("=" * 80)
        print(f"Total found: {result.get('total_count', 'unknown')}")
        return result
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    print("=" * 80)
    print("🔍 CLOUDINARY FOLDER VERIFICATION")
    print("=" * 80)

    # List root folders
    list_folders()

    # Check for Shyam folder
    print("\n" + "=" * 80)
    print("Checking 'Shyam' folder...")
    print("=" * 80)
    list_subfolders("Shyam")

    # Check Shyam/Finest Coating
    print("\n" + "=" * 80)
    print("Checking 'Shyam/Finest Coating' folder...")
    print("=" * 80)
    list_subfolders("Shyam/Finest Coating")

    # List some images from Shyam/Finest Coating
    print("\n" + "=" * 80)
    print("Listing images in 'Shyam/Finest Coating'...")
    print("=" * 80)
    list_resources_in_folder("Shyam/Finest Coating", max_results=5)

    # Check specific section
    print("\n" + "=" * 80)
    print("Checking 'Shyam/Finest Coating/Services' folder...")
    print("=" * 80)
    list_subfolders("Shyam/Finest Coating/Services")

    print("\n✨ Done!\n")

if __name__ == "__main__":
    main()
