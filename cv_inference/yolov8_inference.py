
#TODO make polygons filled with transparant color

import torch
import cv2
import numpy as np
from ssl import _create_unverified_context
from time import time
from ultralytics import YOLO

def main():
    start_time = time()

    _create_default_https_context = _create_unverified_context


    source_video_path = "demovideo.webm"
    #video_saving_path = "output/out1.mp4"

    ################# MODEL CONF ##################
    model = YOLO("yolov8s.pt")  # load an official model


    video_cap=cv2.VideoCapture(source_video_path)

    #fps = video_cap.get(cv2.CAP_PROP_FPS)
    width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #desired_fps = 35
    #result = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v') ,desired_fps, (width,height))


    count=0
    while video_cap.isOpened():
        count += 1    
        ret,frame=video_cap.read()
        if not ret:
            break
        #ADJUST FPS
        if count % 1 != 0:
            continue

        if count >100:
            break

        results = model.predict(source=frame,classes=2)

        for result in results:
            result = result.cpu().numpy()
            for box in result.boxes.xyxyn:
                #print(box)
                x1,y1,x2,y2 = box
                x1,y1,x2,y2 = int(x1*width),int(y1*height),int(x2*width), int(y2*height)

                #print(x1,y2,x2,y2)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            #cv2.putText(frame, str(row['confidence']), (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)








        """for index, row in results.pandas().xyxy[0].iterrows():
            class_name, x1, y1, x2, y2 = row['name'],int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.putText(frame, str(row['confidence']), (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)"""
    
                



        cv2.imshow("ROI",frame)
        print(f"frame {count} writing")
        if cv2.waitKey(10) == ord('q'):
            break


    video_cap.release()
    #result.release()
    cv2.destroyAllWindows()
    print("process done")        
    print("Execution time:", time() - start_time, "seconds")


if __name__ == "__main__":
    main()
#python3 tracker/track.py --yolo-weights yolov8m.pt --source input/deneme1.mp4 --tracking-method ocsort --show-vid --device "mps"
