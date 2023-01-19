import cv2 
import numpy as np 
import os 
import os

# specify the directory containing the text files
folder_path = 'opencv/labels/'

# initialize an empty list to store the detection information
detections = []

for i in range(1, 273):
    # construct the full file name
    filename = "dummies_{}.txt".format(i)
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


cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
video_cap = cv2.VideoCapture("opencv/dummies.mp4")
fps = video_cap.get(cv2.CAP_PROP_FPS)
result = cv2.VideoWriter('babba.mp4', cv2.VideoWriter_fourcc(*'mp4v') ,20.0, (2688,1520))
width, height =  2688, 1520
counter = 1
while video_cap.isOpened():
    success, frame = video_cap.read()
    #print(frame.shape)
    if success:
        for m in range(len(detections[counter-1])):
            cv2.putText(frame, str(counter), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 4) #counter on screen 

            x, y, w, h = detections[counter-1][m][1:5]
            x1, y1, x2, y2 = int((x-w/2)*width), int((y-h/2)*height), int((x+w/2)*width), int((y+h/2)*height)  #xywh to xyxy convertion
            print(x1, y1, x2, y2)
            label = detections[counter-1][m][0]
            if label ==0:
                tag = "FORKLIFT"
            else:
                tag = "WORKER"

            #rect = cv2.rectangle(frame, (x1, y1), (x2,y2), (0,255,0), 5)
            if label ==0:
                if counter>103 and counter<210: #person on lift detected 
                    rect = cv2.rectangle(frame, (x1-100, y1-110), (x2+60,y2+40), (0,0,255), 5)
                    cv2.putText(rect, tag, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                    cv2.putText(rect, "2 PERSON ON LIFT!!", (900,400), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0,0,255), 2)
                else:
                    rect = cv2.rectangle(frame, (x1, y1), (x2,y2), (0,255,0), 5)
                    cv2.putText(rect, tag, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            else:
                rect = cv2.rectangle(frame, (x1, y1), (x2,y2), (0,255,0), 5)
                cv2.putText(rect, tag, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)


        cv2.imshow("frame", rect)
        result.write(frame)
        print(counter)
        counter +=1 
        if cv2.waitKey(20) == ord('q'):
            break
    else:
        break




print("done")
video_cap.release()
result.release()
cv2.destroyAllWindows()
