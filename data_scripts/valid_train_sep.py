import os
import random
import shutil

# Set up directories
main_path = "new_dataset/categorized"
train_dir = "new_dataset/train"
valid_dir = "new_dataset/valid"

if not os.path.exists(train_dir):
    os.mkdir(train_dir)

if not os.path.exists(valid_dir):
    os.mkdir(valid_dir)

for sub_folder in os.listdir(main_path):
    file_list= []
    if sub_folder.startswith("factory"):
        sub_folder = "new_dataset/categorized/"+sub_folder
        # Get a list of all the files with extension .png
        file_list = [f for f in os.listdir(sub_folder) if f.endswith('.png')]

        # Shuffle the list randomly
        random.shuffle(file_list)

        # Calculate the number of files for validation set
        num_valid = int(0.15 * len(file_list))

        # Move files to the validation set directory
        for file_name in file_list[:num_valid]:
            base_name = os.path.splitext(file_name)[0]
            shutil.move(os.path.join(sub_folder, file_name), os.path.join(valid_dir, file_name))
            shutil.move(os.path.join(sub_folder, base_name + '.txt'), os.path.join(valid_dir, base_name + '.txt'))

        # Move files to the training set directory
        for file_name in file_list[num_valid:]:
            base_name = os.path.splitext(file_name)[0]
            shutil.move(os.path.join(sub_folder, file_name), os.path.join(train_dir, file_name))
            shutil.move(os.path.join(sub_folder, base_name + '.txt'), os.path.join(train_dir, base_name + '.txt'))
