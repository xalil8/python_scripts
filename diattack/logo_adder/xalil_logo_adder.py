import cv2
import numpy as np 
#setup
source_video_path = "demos/demo2.mp4"
video_saving_path = source_video_path[:len(source_video_path)-4:]+"_wlogo.mp4"
logo_path = "logo_adder/divisor.png"


def overlayPNG(imgBack, imgFront, pos=[0, 0]):
    hf, wf, cf = imgFront.shape
    hb, wb, cb = imgBack.shape
    *_, mask = cv2.split(imgFront)
    maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    imgRGBA = cv2.bitwise_and(imgFront, maskBGRA)
    imgRGB = cv2.cvtColor(imgRGBA, cv2.COLOR_BGRA2BGR)

    imgMaskFull = np.zeros((hb, wb, cb), np.uint8)
    imgMaskFull[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = imgRGB
    imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255
    maskBGRInv = cv2.bitwise_not(maskBGR)
    imgMaskFull2[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = maskBGRInv

    imgBack = cv2.bitwise_and(imgBack, imgMaskFull2)
    imgBack = cv2.bitwise_or(imgBack, imgMaskFull)

    return imgBack

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_cap = cv2.VideoCapture(source_video_path)

width, height = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter(video_saving_path, cv2.VideoWriter_fourcc(*'mp4v') ,video_cap.get(cv2.CAP_PROP_FPS), (width,height))
print(width,height,"##########################")

logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

k = 1 if width<1500 else 2 

logo_x = 200 *k
logo_y = 48 *k
logo = cv2.resize(logo, (logo_x,logo_y)) #200, 48

counter =0
while video_cap.isOpened():
    ret, frame = video_cap.read()
    if not ret:
        break

    if ret:

        frame = overlayPNG(frame, logo, [width-logo_x-50, height-logo_y-50])  #1050, 650

        
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
