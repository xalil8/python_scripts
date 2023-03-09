import torch
import cv2
import numpy as np
from ssl import _create_unverified_context
from time import time
import os 

_create_default_https_context = _create_unverified_context

model = torch.hub.load("ultralytics/yolov5","custom",path="weights/genel_model.pt",force_reload=False)
model.to(torch.device("mps"))
model.conf = 0.6

def pascal_voc_to_yolo(x1, y1, x2, y2, image_w, image_h):



    return [((x2 + x1)/(2*image_w)), ((y2 + y1)/(2*image_h)), (x2 - x1)/image_w, (y2 - y1)/image_h]


path = "val/images"
output_path = "val/labels2"
count = 0

# Loop through all images in folder
for img_name in os.listdir(path):
    # Read image
    if os.path.splitext(img_name)[1].lower() not in ('.jpg', '.png'):
        continue
    img_path = os.path.join(path, img_name)
    label_path = os.path.join(output_path, os.path.splitext(img_name)[0] + ".txt")

    # Check if the label file already exists
    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            lines = f.readlines()
    else:
        lines = []

    frame = cv2.imread(img_path)
    count += 1

    #ADJUST FPS
    if count % 1 != 0:
        continue

    results = model(frame)
    
    for index, row in results.pandas().xyxy[0].iterrows():
        class_name, x1, y1, x2, y2 = row['name'],int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        if class_name != "insan":
            continue

        cv2.rectangle(frame,(x1-10,y1-10),(x2+10,y2+10),(255,0,0),2)
        cv2.putText(frame, str(row["confidence"]), (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

        x,y,w,h = pascal_voc_to_yolo(x1, y1, x2, y2, 1920, 1080)
        new_class_value = 1
        lines.append(f"{new_class_value} {x} {y} {w} {h}\n")

    # Write the updated lines to the label file
    with open(label_path, "w") as f:
        f.writelines(lines)

    cv2.imshow("ROI",frame)
    print(f"frame {count} writing")

    if cv2.waitKey(1000) == ord('q'):
        break

cv2.destroyAllWindows()
print("process done")
