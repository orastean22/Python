# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 30/10/2024
# -- Update on 30/10/2024 - not working yet
# -- Author: AdrianO
# -- Version 0.1 - Draft code to open the files and read Exif info for each photo
# --                - Open and travel to directory to find images folder.
# --                - Extract EXIF metadata from each image.
# --                - Display the EXIF data
# --                - Compare key EXIF tags to identify duplicates.
# --                - Retain the first file in each duplicate group and delete the rest.
# --                - Confirm deletion with a print message for each file removed.
# --                - Display duplicates side-by-side
# --                - Add a confirmation before deletion: Allow the user to confirm whether they want to delete the duplicates
# -- Script Task: detect duplicate photos based on their EXIF metadata
# -- pip install exifread; pip install matplotlib

import os
import hashlib
from PIL import Image
from collections import defaultdict
from tkinter import Tk, filedialog
import matplotlib.pyplot as plt

# **********************************************************************************
# Generates a checksum for the file based on its content using the specified algorithm
# **********************************************************************************
def find_duplicate_images_by_checksum(directory, algorithm="sha256"):
    checksum_dict = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg', 'png')):
                filepath = os.path.join(root, file)
                try:
                    file_checksum = get_file_checksum(filepath, algorithm=algorithm)
                    checksum_dict[file_checksum].append(filepath)
                except Exception as e:
                    print(f"Error calculating checksum for {filepath}: {e}")

    # Filter groups to only those with duplicates
    duplicates = [files for files in checksum_dict.values() if len(files) > 1]
    return duplicates

# **********************************************************************************
# Generates a checksum for the file based on its content using the specified algorithm
# **********************************************************************************
def get_file_checksum(filepath, algorithm="sha256"):

    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


# **********************************************************************************
# Delete Duplicates function with user confirmation
# **********************************************************************************
def delete_duplicates(duplicates):
    for group in duplicates:
        print("\nDo you want to delete duplicates in this group? (y/n)")
        display_duplicates([group])  # Display images side-by-side
        confirm = input("Delete duplicates and keep only one? (y/n): ").strip().lower()
        if confirm == 'y':
            # Keep the first file, delete the rest
            for filepath in group[1:]:  # Only delete files starting from the second
                try:
                    os.remove(filepath)
                    print(f"Deleted duplicate: {filepath}")
                except Exception as e:
                    print(f"Error deleting file {filepath}: {e}")
        else:
            print("Skipping deletion for this group.")

# **********************************************************************************
# Main function
# **********************************************************************************
def main():
    # Open a file dialog to select directory
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Folder with Images")

    if directory:
        # Run the duplicate finding function
        duplicates = find_duplicate_images_by_checksum(directory)

        if duplicates:
            print("\nReview duplicates before deletion:")
            delete_duplicates(duplicates)
        else:
            print("No duplicates found.")
    else:
        print("No directory selected.")

if __name__ == "__main__":
    main()