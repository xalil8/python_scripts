
#TODO make polygons filled with transparant color

import torch
import cv2
import numpy as np
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


source_video_path = "polyline/polygon.mp4"
video_saving_path = source_video_path[:len(source_video_path)-4:]+"_output.mp4"

polygon_points = np.array( [[446, 599], [575, 559], [1217, 954], [1273, 832], [592, 465], [507, 485], [130, 237], [66, 248]])
model = torch.hub.load("ultralytics/yolov5","custom",path="polyline/best.pt",force_reload=True)


#to use with default yolo model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

video_cap=cv2.VideoCapture(source_video_path)

fps = video_cap.get(cv2.CAP_PROP_FPS)
width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

desired_fps = 20
result = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v') ,desired_fps, (width,height))


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
    cv2.polylines(frame, np.int32([polygon_points]), True, (255,0,0),3)

    for index, row in results.pandas().xyxy[0].iterrows():
        class_name, x1, y1, x2, y2 = row['name'],int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        if class_name =="insan":
            center_x, center_y = int((x1+x2)/2), y2

            area_check = cv2.pointPolygonTest(np.int32([polygon_points]),((center_x,center_y)), False)

            #if person are in polygon (safe) area 
            if area_check ==1:
                #cv2.circle(frame,(center_x,center_y),3,(255,0,0),-1)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame, class_name, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

            #person are in danger zone 
            else:
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.putText(frame, class_name, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                cv2.putText(frame, "TEHLIKELI BOLGEDE INSAN VAR", (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)



    cv2.imshow("ROI",frame)
    print(f"frame {count} writing")
    result.write(frame)


    if cv2.waitKey(1) == ord('q'):
        break


video_cap.release()
result.release()
cv2.destroyAllWindows()
print("process done")
