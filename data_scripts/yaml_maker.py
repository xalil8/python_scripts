import os
import shutil

"""
    Create the necessary yaml file with a specified classes.txt file
"""


# read classes.txt
with open('classes.txt', 'r') as f:
    classes = f.readlines()
    classes = [c.strip() for c in classes]

length = len(classes)
print(length)

yaml_template = """
train: ../output/images/train  # train images (relative to 'path') 128 images
val: ../output/images/val  # val images (relative to 'path') 128 images
test:  # test images (optional)\n
"""

yaml_template = yaml_template + f"nc: {length} # number of classes \n"
# add newline to end of each class
yaml_template = yaml_template + f"names: {classes} # class names"


# delete the file if it exists
# and create a new one
if os.path.exists('custom_data.yaml'):
    os.remove('custom_data.yaml')
with open('custom_data.yaml', 'w') as f:
    f.write(yaml_template)
