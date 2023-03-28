
#TODO make polygons filled with transparant color

import torch
import cv2
import numpy as np
from ssl import _create_unverified_context
from time import time
start_time = time()

_create_default_https_context = _create_unverified_context


source_video_path = "videos/onluk_deneme.mp4"
video_saving_path = "output/onluk_deneme_output.mp4"

#video_saving_path = source_video_path[:len(source_video_path)-4:]+"_output.mp4"

#polygon_points_1 = np.array( [[1264, 788], [605, 442], [519, 463], [143, 237], [68, 245], [458, 595], [581, 558], [1181, 936]])

#polygon_points_2 = np.array( [[913, 485], [1141, 389], [602, 189], [433, 244]])



model = torch.hub.load("ultralytics/yolov5","custom",path="weights/onluk_renk.pt",force_reload=False)
model.to(torch.device("mps"))
model.conf = 0.7
#to use with default yolo model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

video_cap=cv2.VideoCapture(source_video_path)
#fps = video_cap.get(cv2.CAP_PROP_FPS)
#width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#desired_fps = 35
#result = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v') ,desired_fps, (width,height))


count=0
while video_cap.isOpened():
    ret,frame=video_cap.read()

    if not ret:
        break
    #ADJUST FPS
    count += 1
    if count % 1 != 0:
        continue

    results = model(frame)
#    cv2.polylines(frame, np.int32([polygon_points_1]), True, (255,0,0),3)
#    cv2.polylines(frame, np.int32([polygon_points_2]), True, (240,0,0),3)

    for index, row in results.pandas().xyxy[0].iterrows():
        class_name, x1, y1, x2, y2 = row['name'],int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        """if class_name =="mavi_onluk":
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
            cv2.putText(frame, str(row["confidence"]), (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
        elif class_name =="turuncu_onluk":
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.putText(frame, str(row["confidence"]), (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)"""
        
        bias_y =int((y2-y1)/2*0.7)
        bias_x =int((x2-x1)/2*0.7)         
        cv2.imshow("ROI",frame[y1+bias_y:y2-bias_y,x1+bias_x:x2-bias_x])
        
    print(f"frame {count} writing")
    #result.write(frame)


    if cv2.waitKey(1) == ord('q'):
        break


video_cap.release()
#result.release()
cv2.destroyAllWindows()
print("process done")
print("Execution time:", time() - start_time, "seconds")
