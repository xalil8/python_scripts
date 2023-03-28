import os
import shutil

directory = "all"
file_list = "bad_files.txt"
destination_dir = "trash_images"

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Read the list of filenames from the filelist.txt file
with open(file_list, "r") as f:
    filenames = f.read().splitlines()

# Loop through all the files in the directory
for filename in os.listdir(directory):
    # Check if the current file is in the list of filenames to move
    if filename in filenames:
        # Move the file to the destination directory
        shutil.move(os.path.join(directory, filename), os.path.join(destination_dir, filename))


print("done")
