#area = [[467, 422], [533, 407], [150, 199], [118, 206]]

#TODO make polygons filled with transparant color

import torch
import cv2
import numpy as np
import ssl
#points = np.array([[112, 278], [463, 573], [575, 537], [1136, 891], [1185, 821], [601, 489], [504, 510], [149, 269]])
#points = np.array([[110, 275], [435, 566], [558, 537], [154, 271]])
points = np.array([[86, 258], [422, 595], [563, 565], [1139, 926], [1215, 802], [606, 459], [507, 481], [153, 257]])
#points = points.reshape((-1,1,2))
ssl._create_default_https_context = ssl._create_unverified_context

source_video_path = "custom_plot/deneme2.mp4"

video_cap=cv2.VideoCapture('polyline/polygon.mp4')

#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

model = torch.hub.load("ultralytics/yolov5","custom",path="polyline/best.pt",force_reload=True)




count=0
while video_cap.isOpened():
    ret,frame=video_cap.read()

    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue

    #roi = frame[200:400,200:400]
    results = model(frame)
    cv2.polylines(frame, np.int32([points]), True, (255,0,0),3)

    for index, row in results.pandas().xyxy[0].iterrows():
        class_name, x1, y1, x2, y2 = row['name'],int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        if class_name =="insan":
            center_x, center_y = int((x1+x2)/2), y2

            area_check = cv2.pointPolygonTest(np.int32([points]),((center_x,center_y)), False)

            if area_check ==1:
                #cv2.circle(frame,(center_x,center_y),3,(255,0,0),-1)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame, class_name, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)


            else:
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.putText(frame, class_name, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)



    #cv2.polylines(frame,np.array(area,np.int32),True, (0,0,255),2)
    cv2.imshow("ROI",frame)



    if cv2.waitKey(1) == ord('q'):
        break


video_cap.release()
cv2.destroyAllWindows()
