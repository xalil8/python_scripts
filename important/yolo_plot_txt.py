import cv2 
import numpy as np 
import os 
import os

# specify the directory containing the text files
folder_path = "custom_plot/labels"
#source_video_path = "custom_plot/deneme2_output.mp4"
source_video_path = "custom_plot/deneme2.mp4"

video_saving_path = source_video_path[:len(source_video_path)-4:]+"_output.mp4"



detections = []

file_list = os.listdir(folder_path)
for i in range(1, len(file_list)+1):
    # construct the full file name
    prefix = file_list[0].rsplit("_", 1)[0]
    filename = f"{prefix}_{i}.txt"
    filepath = os.path.join(folder_path, filename)
    # read the contents of the text file
    with open(filepath, 'r') as file:
        detection_frame = []
        # loop through each line of the text file
        for line in file:
            # split the line into a list of values
            values = line.strip().split()
            # convert the values to integers or floats as necessary
            values = [int(values[0]), float(values[1]), float(values[2]), float(values[3]), float(values[4])]
            # add the values to the detections list
            detection_frame.append(values)
        detections.append(detection_frame)
print("TXT PROCESS DONE")

#######################VIDEO PROCESSING ################################
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
video_cap = cv2.VideoCapture(source_video_path)
fps = video_cap.get(cv2.CAP_PROP_FPS)
width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

result = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v') ,20.0, (width,height))
counter = 1


while video_cap.isOpened():
    success, frame = video_cap.read()
    #print(frame.shape)
    if success:
        for m in range(len(detections[counter-1])):
            cv2.putText(frame, str(counter), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 4) #counter on screen 

            x, y, w, h = detections[counter-1][m][1:5]
            x1, y1, x2, y2 = int((x-w/2)*width), int((y-h/2)*height), int((x+w/2)*width), int((y+h/2)*height)  #xywh to xyxy convertion
            #print(x1, y1, x2, y2)
            
            label = detections[counter-1][m][0]
            if label ==0:
                tag = "MASKE VAR"
                
            #rect = cv2.rectangle(frame, (x1, y1), (x2,y2), (0,255,0), 5)

            if label == 0:
                rect = cv2.rectangle(frame, (x1, y1), (x2,y2), (0,255,0), 2)
                cv2.putText(rect, tag, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)



        cv2.imshow("frame", rect)
        result.write(rect)
        print(counter)
        counter +=1 
        if cv2.waitKey(30) == ord('q'):
            break
    else:
        break


print("done")
video_cap.release()
result.release()
cv2.destroyAllWindows()
