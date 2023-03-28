import os
import random
import shutil

# Define the paths to the folders containing the images and labels
image_folder = "diffusor_new_dataset/images"
label_folder = "diffusor_new_dataset/labels_without_sigara"

# Define the percentage split between train, valid, and test sets
train_percent = 80
valid_percent = 15
test_percent = 5

# Define the paths to the output folders for the train, valid, and test sets
train_folder = "split_dataset/train"
valid_folder = "split_dataset/valid"
test_folder =  "split_dataset/test"

# Create the output folders if they don't exist
os.makedirs(train_folder, exist_ok=True)
os.makedirs(valid_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# Get a list of all the image files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(".png")]

# Shuffle the list of image files randomly
random.shuffle(image_files)

# Calculate the number of images for each set based on the percentages
num_images = len(image_files)
num_train = int(num_images * train_percent / 100)
num_valid = int(num_images * valid_percent / 100)
num_test = int(num_images * test_percent / 100)

# Copy the first num_train images to the train folder, along with their corresponding label files
for i in range(num_train):
    image_file = image_files[i]
    label_file = os.path.splitext(image_file)[0] + ".txt"
    shutil.copy(os.path.join(image_folder, image_file), os.path.join(train_folder, image_file))
    shutil.copy(os.path.join(label_folder, label_file), os.path.join(train_folder, label_file))

# Copy the next num_valid images to the valid folder, along with their corresponding label files
for i in range(num_train, num_train + num_valid):
    image_file = image_files[i]
    label_file = os.path.splitext(image_file)[0] + ".txt"
    shutil.copy(os.path.join(image_folder, image_file), os.path.join(valid_folder, image_file))
    shutil.copy(os.path.join(label_folder, label_file), os.path.join(valid_folder, label_file))

# Copy the remaining num_test images to the test folder, along with their corresponding label files
for i in range(num_train + num_valid, num_images):
    image_file = image_files[i]
    label_file = os.path.splitext(image_file)[0] + ".txt"
    shutil.copy(os.path.join(image_folder, image_file), os.path.join(test_folder, image_file))
    shutil.copy(os.path.join(label_folder, label_file), os.path.join(test_folder, label_file))


print("done")
