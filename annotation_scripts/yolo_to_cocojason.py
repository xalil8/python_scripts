import json
import os
import cv2

# Define the paths to the YOLO label directory and COCO label file
yolo_label_dir = "split_dataset/test"
coco_label_file = "test.json"

# Define the class names
class_names = ["forkliftkamyon","insan","baret_var","baret_yok","kedi","kopek", "palet" ]

# Create the COCO label data structure
coco_label_data = {
    "info": {},
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": [{"id": i+1, "name": class_names[i]} for i in range(len(class_names))]
}

# Iterate through the YOLO label files and convert the labels to COCO format
image_id = 1
annotation_id = 1
counter = 0
for filename in os.listdir(yolo_label_dir):
    if filename.endswith(".txt"):
        counter += 1
        print(counter)


        yolo_label_file = os.path.join(yolo_label_dir, filename)
        image_file = os.path.splitext(filename)[0] + ".jpg"
        image_path = os.path.join(yolo_label_dir, image_file)
        if not os.path.isfile(image_path):
            continue
        image = cv2.imread(image_path)
        image_height, image_width, _ = image.shape
        with open(yolo_label_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 5:
                    continue
                x_center = float(parts[1]) * image_width
                y_center = float(parts[2]) * image_height
                width = float(parts[3]) * image_width
                height = float(parts[4]) * image_height
                x_min = x_center - width / 2
                y_min = y_center - height / 2
                coco_label_data["images"].append({
                    "id": image_id,
                    "file_name": image_file,
                    "width": image_width,
                    "height": image_height
                })
                coco_label_data["annotations"].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": int(parts[0]),
                    "bbox": [x_min, y_min, width, height],
                    "area": width * height,
                    "iscrowd": 0
                })
                annotation_id += 1
            image_id += 1

# Write the COCO label data to a JSON file
with open(coco_label_file, "w") as f:
    json.dump(coco_label_data, f)

print("process done")