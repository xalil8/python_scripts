 

import cv2
import numpy as np
from time import time
start_time = time()



source_video_path = "double_polygon.mp4"
video_saving_path = "output_double_polygon.mp4"




video_cap=cv2.VideoCapture(source_video_path)

fps = video_cap.get(cv2.CAP_PROP_FPS)
width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

desired_fps = 35
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



    #1280 x 960 
    cv2.putText(frame, "________", (10,860), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 8)
    cv2.putText(frame, "=GUVENLI ALAN", (130,870), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 4)

    cv2.putText(frame, "________", (10,900), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 8)
    cv2.putText(frame, "=IHLAL YOK", (130,910), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 4)

    cv2.putText(frame, "________", (10,940), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 8)
    cv2.putText(frame, "=IHLAL VAR", (130,950), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 4)


    cv2.imshow("ROI",frame)
    print(f"frame {count} writing")
    result.write(frame)


    if cv2.waitKey(1) == ord('q'):
        break


video_cap.release()
result.release()
cv2.destroyAllWindows()
print("process done")
print("Execution time:", time() - start_time, "seconds")
