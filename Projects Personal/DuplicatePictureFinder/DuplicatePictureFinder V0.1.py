
# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 30/10/2024
# -- Update on 30/10/2024 - not working yet
# -- Author: AdrianO
# -- Version 0.1 - Draft code to open the files and read Exif info for each photo
# --                - Traverse a directory to find all images.
# --                - Extract EXIF metadata from each image.
# --                - Compare key EXIF tags to identify duplicates.
# --                - Optionally, move or delete duplicate files.
# -- Script Task: detect duplicate photos based on their EXIF metadata
# -- pip install pillow exifread

import os
from PIL import Image
import exifread
from collections import defaultdict


def get_exif_data(filepath):
    """Extracts EXIF data from an image file."""
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f, details=False)

        # Define the key EXIF tags you want to compare
        exif_keys = ['EXIF DateTimeOriginal', 'Image Make', 'Image Model', 'EXIF FocalLength']
        exif_data = {key: tags.get(key) for key in exif_keys if key in tags}

        return exif_data


def find_duplicate_images(directory):
    """Finds and prints duplicate images based on EXIF data."""
    exif_dict = defaultdict(list)

    # Walk through directory and process each image file
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg', 'png')):
                filepath = os.path.join(root, file)

                try:
                    exif_data = get_exif_data(filepath)
                    exif_tuple = tuple(exif_data.items())
                    exif_dict[exif_tuple].append(filepath)

                except Exception as e:
                    print(f"Error reading EXIF data for {filepath}: {e}")

    # Display duplicates
    duplicates = [files for files in exif_dict.values() if len(files) > 1]
    for group in duplicates:
        print("Duplicate group:")
        for filepath in group:
            print(f"  {filepath}")

    return duplicates


# Run the function on a target directory
directory = '/path/to/your/folder'
duplicates = find_duplicate_images(directory)

# Optionally: Delete or move duplicates (be cautious!)
# for group in duplicates:
#     for filepath in group[1:]:  # Keep the first file, delete others
#         os.remove(filepath)