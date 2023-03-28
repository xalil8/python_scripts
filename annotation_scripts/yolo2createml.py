import os
import json
import cv2

# Define the class names corresponding to each label index
class_names = ["class1","class2","class3"...]
 
#final json file name
json_name = "xxxx.json"
#folder should contains all images and files in same folder with same name 
#if you use jpg or other image types than png, change line 46
directory = "path"

# Function to convert YOLO bounding box coordinates to Core ML format
def convert_yolo_to_coreml(x, y, w, h, image_width, image_height):
    # Convert x and w from YOLO format to pixel coordinates
    pixel_x = x * image_width
    pixel_w = w * image_width

    # Convert y and h from YOLO format to pixel coordinates
    pixel_y = y * image_height
    pixel_h = h * image_height

    # Calculate the x, y, w, h values for Core ML format
    coreml_x = pixel_x + (pixel_w / 2)
    coreml_y = pixel_y + (pixel_h / 2)
    coreml_w = pixel_w
    coreml_h = pixel_h

    return (round(coreml_x,2), round(coreml_y,2), round(coreml_w,2), round(coreml_h,2))



# Create an empty dictionary to store the CreateML JSON data
create_ml_data = []

# Loop over all the txt files in the directory
counter = 0
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        counter +=1 
        print(counter)
        # Open the YOLO txt file
        with open(os.path.join(directory, filename), 'r') as f:
            yolo_data = f.readlines()

        # Load the image using OpenCV to get its dimensions
        image_filename = os.path.splitext(filename)[0] + ".png"
        image_path = os.path.join(directory, image_filename)
        image = cv2.imread(image_path)
        image_height, image_width, _ = image.shape

        # Create an empty list to store the annotations for this image
        annotations = []

        # Loop over each line in the YOLO txt file
        for line in yolo_data:
            # Extract the label index and bounding box coordinates
            label_index, x, y, w, h = line.strip().split()
            label_index, x, y, w, h = int(label_index), float(x), float(y), float(w), float(h)

            # Convert the bounding box coordinates to Core ML format
            coreml_x, coreml_y, coreml_w, coreml_h = convert_yolo_to_coreml(x, y, w, h, image_width, image_height)
            coordinates = {"x": coreml_x, "y": coreml_y, "width": coreml_w, "height": coreml_h}

            # Get the class name corresponding to the label index
            label = class_names[label_index]

            # Add the bounding box data to the list of annotations
            annotations.append({"label": label,"coordinates": coordinates})

        # Add the annotations for this image to the CreateML JSON data dictionary

        create_ml_data.append({"image":image_filename,"annotations":annotations})

# Save the CreateML JSON data to a single file
with open(json_name, 'w') as f:
    json.dump(create_ml_data, f)

print("CONVERTING PROCESS DONE  !!")


