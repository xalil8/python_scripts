import time
import cv2
import numpy as np

from FiveS import FiveS  # Import the FiveS class from the FiveS module
class CameraStorage:
    def __init__(self):
        
        self.camera_id = "1"
        # untouched frame
        self.original_live_frame = None

        # violations drawn frame
        self.violation_live_frame = None
        # font
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.font_scale = 1

        self.violation_font_color = (0, 0, 255)

        self.violation_font_ticknes = 2

        self.violation_line_type = cv2.LINE_AA

        self.violation_save_path = "file_violation"
        
        



if __name__ == "__main__":
    # Define camera data for a single camera and polygon
    print("code has started")
    
    #"ConnectionStr": "rtsp://admin:Welc0me12@192.168.1.5:554/Streaming/Channels/1/",
    connectionStr =  "distance.mp4"
    poly =  np.array([[973, 354], [15, 1231], [2472, 1193], [1524, 332]]).reshape(-1,1,2)

    # Create an instance of the Camera class

    storage = CameraStorage()
    
    five_s = FiveS(poly,storage)

    video_cap = cv2.VideoCapture(connectionStr)
    
    while video_cap.isOpened():
        ret, frame = video_cap.read()
        if not ret:
            break
        frame = cv2.resize(frame,(1280,720))
        
        
        storage.original_live_frame =  frame
        
        #storage.violation_live_frame = frame.copy()
        
        thresh = five_s.main(False)

        
        # # Display both the raw frame and the processed frame side by side
        # frames = np.hstack((camera_instance.storage.original_live_frame, camera_instance.storage.violation_live_frame))
        # frames = cv2.resize(frames, (1500,720))
        cv2.imshow("Raw Frame vs Processed Frame", thresh)
        cv2.waitKey(30)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
