import easyocr
import cv2
import matplotlib.pyplot as plt
import torch

#path your video 
video_path = "C:/Users/halil/Desktop/video_process/car_video.mp4"
my_video = cv2.VideoCapture(video_path)

#create tracbars 
cv2.namedWindow('controls',cv2.WINDOW_NORMAL)
cv2.namedWindow("screen",cv2.WINDOW_NORMAL)
cv2.resizeWindow('controls',600,300)
cv2.resizeWindow('screen',720,480)
cv2.createTrackbar('Blur','controls',0,20,lambda x:x)
cv2.createTrackbar('Blur Iteration','controls',0,10,lambda x:x)
cv2.createTrackbar('Threshold Block Size','controls', 222, 255, lambda x:x)
cv2.createTrackbar('Threshold Constant','controls', 20, 255, lambda x:x)
cv2.createTrackbar('Threshold Flag','controls', 2, 5, lambda x:x)
cv2.createTrackbar('BITWISE ON OFF','controls', 0, 1, lambda x:x)
cv2.createTrackbar('ADAPTIVE TH','controls', 0, 1, lambda x:x)


#this function to choose threshold type (flag)
def th_key_maker(key):
    if key == 1:
        #print("cv2.THRESH_BINARY_INV")
        return cv2.THRESH_BINARY_INV
    elif key == 2:
        #print("cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU")
        return cv2.THRESH_BINARY_INV
        #return cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    elif key == 3:
        #print("cv2.THRESH_TOZERO")
        return cv2.THRESH_TOZERO
    elif key == 4:
        #print("cv2.THRESH_TOZERO_INV")
        return cv2.THRESH_TOZERO_INV
    elif key == 5:
        #print("cv2.THRESH_TRUNC")
        return cv2.THRESH_TRUNC
    else:
        #print("cv2.THRESH_BINARY")
        return cv2.THRESH_BINARY


while True:
    #reading image frame by frame 
    _, img = my_video.read()
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #controlling values through trackbar 
    blur = int(cv2.getTrackbarPos('Blur', 'controls'))
    blur_it = int(cv2.getTrackbarPos('Blur Iteration', 'controls'))
    th1 = int(cv2.getTrackbarPos('Threshold Block Size', 'controls'))
    th2 = int(cv2.getTrackbarPos('Threshold Constant', 'controls'))
    th_key_num = int(cv2.getTrackbarPos('Threshold Flag', 'controls'))
    bitwise_on_off = int(cv2.getTrackbarPos('BITWISE ON OFF', 'controls'))
    adaptive_to_normal = int(cv2.getTrackbarPos('ADAPTIVE TH', 'controls'))
    th_key = th_key_maker(th_key_num)
    
    # for avoiding crash, blur values should bigger than 3 and even number
    while blur % 2 == 0 or blur <3:
        blur += 1
    while th1 % 2 == 0 or th1 < 2:
        th1 += 1
    while th2 % 2 == 0:
        th2 += 1

    #applying blur
    blurred = cv2.medianBlur(img,blur)
    blurred = cv2.GaussianBlur(img, (blur, blur), blur_it)
    grey_blurred = cv2.GaussianBlur(img_grey, (blur, blur), blur_it)
    
    #applying threshold
    if adaptive_to_normal:
        threshold = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,th1,th2)
    else:
        qret, threshold = cv2.threshold(blurred, th1, th2, th_key)
        #ret, threshold = cv2.threshold(blurred, th1, th2, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    #applying binarization on image
    if bitwise_on_off:
        bitwise = cv2.bitwise_not(threshold)
    else:
        bitwise = threshold

    
    #show video, frame by frame 
    cv2.imshow("screen", bitwise)

    #press 'q' to stop program
    # waitkey value adjust run speed of video, bigger number is slower video
    if cv2.waitKey(28) & 0xFF == ord('q'):
        break

my_video.release()
cv2.destroyAllWindows()