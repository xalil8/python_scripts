import torch
import cv2
import numpy as np
import ssl
import concurrent.futures
import time
start_time = time.time()




#PATH CONFIGURATION
source_video_path = "input_videos/short_raw.mp4"
video_saving_path = source_video_path[:len(source_video_path)-4:]+"_output5.mp4"

#ML MODEL CONFIGURATION
ssl._create_default_https_context = ssl._create_unverified_context
model = torch.hub.load("ultralytics/yolov5","custom",path="models/genel_model.pt",force_reload=False)

#VIDEO CONFIGURATION
video_cap = cv2.VideoCapture(source_video_path)
fps = video_cap.get(cv2.CAP_PROP_FPS)
width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
desired_fps = 30
result = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v'), desired_fps, (width, height))

count = 0

def process_frame(frame):
    results = model(frame)

    for index, row in results.pandas().xyxy[0].iterrows():
        class_name, x1, y1, x2, y2 = row['name'],int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        if class_name =="baret_yok":
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.putText(frame, class_name, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        elif class_name =="baret_var":
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame, class_name, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        elif class_name == "insan":
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
            cv2.putText(frame, class_name, (x1,y2+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

        else :
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
            cv2.putText(frame, class_name, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    result.write(frame)


while video_cap.isOpened():
    ret, frame = video_cap.read()

    if not ret:
        break

    # ADJUST FPS
    count += 1
    if count % 1 != 0:
        continue

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(process_frame, frame)
        future.result()




    # cv2.imshow("ROI", result_frame)
    #result.write(result_frame)
    print(f"frame {count} writing")

    if cv2.waitKey(1) == ord('q'):
        break

video_cap.release()
result.release()
cv2.destroyAllWindows()
print("process done")

print("Multi Thread time:", time.time() - start_time, "seconds")

