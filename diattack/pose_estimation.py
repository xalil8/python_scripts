import cv2 
import numpy as np 

video_cap = cv2.VideoCapture("slowed.mp4")

fps = video_cap.get(cv2.CAP_PROP_FPS)

result = cv2.VideoWriter('babba.mp4', cv2.VideoWriter_fourcc(*'mp4v') ,20.0, (2688,1536))

counter = 0
while video_cap.isOpened():
    success, frame = video_cap.read()


    if success:
        if counter >300 and counter < 380:
            if counter %4 == 0:
                rect = cv2.rectangle(frame, (1700, 800), (1900, 1200), (0,0,255), 5)
                cv2.putText(rect, 'ATTENTION', (1700, 750), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)


        #cv2.imshow("frame", frame)
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
