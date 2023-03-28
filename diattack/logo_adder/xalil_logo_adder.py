import cv2
import cvzone

#setup
source_video_path = "logo_adder/new_polygon_polygon.mp4"
video_saving_path = source_video_path[:len(source_video_path)-4:]+"_final_logo.mp4"
logo_path = "logo_adder/divisor.png"



fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_cap = cv2.VideoCapture(source_video_path)

width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v') ,video_cap.get(cv2.CAP_PROP_FPS), (width,height))


logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
logo = cv2.resize(logo, (200, 48)) #200, 48

counter =0
while video_cap.isOpened():
    ret, frame = video_cap.read()
    if not ret:
        break

    if ret:

        frame = cvzone.overlayPNG(frame, logo, [3700, 1300])  #1050, 650

        
        counter +=1
        print(f"frame{counter}processed")
        #cv2.imshow("test", frame)
        writer.write(frame)


    if cv2.waitKey(1) == ord('q'):
        break
    

video_cap.release()
writer.release()
cv2.destroyAllWindows()
print("process done")