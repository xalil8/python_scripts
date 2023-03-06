
import threading
import torch
import cv2
import numpy as np
import ssl
from multiprocessing import Process
import time
start_time = time.time()


class xalil:
      
    def __init__(self):
        
        self.source_video_path = "input_videos/short_raw.mp4"
        self.video_saving_path = self.source_video_path[:len(self.source_video_path)-4:]+"_output5.mp4"

        #ML MODEL CONFIGURATION
        ssl._create_default_https_context = ssl._create_unverified_context
        self.model = torch.hub.load("ultralytics/yolov5","custom",path="models/genel_model.pt",force_reload=False)

        #VIDEO CONFIGURATION
        self.video_cap = cv2.VideoCapture(self.source_video_path)
        fps = self.video_cap.get(cv2.CAP_PROP_FPS)
        width, height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        desired_fps = 30
        self.result = cv2.VideoWriter(self.video_saving_path, cv2.VideoWriter_fourcc(*'mp4v'), desired_fps, (width, height))

        self.count = 0

    def proces1(self):

        results = self.model(self.frame)

        for index, row in results.pandas().xyxy[0].iterrows():
            class_name, x1, y1, x2, y2 = row['name'],int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

            
            cv2.rectangle(self.frame,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.putText(self.frame, class_name, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        self.result.write(self.frame) 
    
    def mainy(self):
        while self.video_cap.isOpened():
            ret, self.frame = self.video_cap.read()

            if not ret:
                break
            
            self.proces1()
            
            # cv2.imshow("ROI", result_frame)
            #result.write(result_frame)
            self.count += 1
            print(f"frame {self.count} writing")

            if cv2.waitKey(1) == ord('q'):
                break

        self.video_cap.release()
        self.result.release()
        cv2.destroyAllWindows()

    

if __name__ == "__main__":

    xalo = xalil()

    xalo.mainy()
    
    print("process done")

    print("Time:", time.time() - start_time, "seconds")
	# creating threads

