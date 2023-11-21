import cv2
import os

def crop_image(image_path, output_path, crop_height):
    """
    Crop the image from the top by the specified height and save the cropped image.
    """
    image = cv2.imread(image_path)
    cropped_image = image[crop_height:,:]  # Crop from the top
    cv2.imwrite(output_path, cropped_image)

def adjust_labels(label_path, output_label_path, crop_height, original_height, new_height):
    """
    Adjust labels for the cropped images.
    Subtract the crop height from the y-coordinate of the bounding box center,
    then normalize it for the new image height.
    """
    with open(label_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 5:
            # Convert y_center to absolute coordinates and adjust
            y_center = float(parts[2]) * original_height
            y_center -= crop_height

            # Only keep the label if it's still within the new image bounds
            if y_center > 0 and y_center < new_height:
                # Normalize the y_center for the new image height
                y_center /= new_height
                parts[2] = str(y_center)
                new_line = ' '.join(parts) + '\n'
                new_lines.append(new_line)

    # Write the modified labels back to the file
    with open(output_label_path, 'w') as file:
        file.writelines(new_lines)

# Directories and settings
input_dir = "all_data"  # Contains both images and labels
output_dir = "out_data"  # Where cropped images and modified labels will be saved
crop_height = 170  # Height in pixels to crop from the top
original_image_height = 1080  # Original image height
new_image_height = original_image_height - crop_height  # New image height after cropping

# Process images and labels
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)

    if filename.endswith('.jpg'):
        # Crop and save images
        crop_image(file_path, output_path, crop_height)
    elif filename.endswith('.txt'):
        # Adjust and save label files
        adjust_labels(file_path, output_path, crop_height, original_image_height, new_image_height)
