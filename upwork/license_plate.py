import cv2
import pytesseract
# import numpy as np
import easyocr


def goruntuisleme(img):
    print("llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")

    cv2.namedWindow("showup", cv2.WINDOW_NORMAL)
    cv2.namedWindow('controls', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('controls', 850, 250)
    cv2.resizeWindow('showup', 850, 250)

    cv2.createTrackbar('Blur', 'controls', 0, 20, lambda x: x)
    cv2.createTrackbar('Blur Iteration', 'controls', 0, 10, lambda x: x)
    cv2.createTrackbar('Threshold Block Size', 'controls', 222, 255, lambda x: x)
    cv2.createTrackbar('Threshold Constant', 'controls', 20, 255, lambda x: x)
    cv2.createTrackbar('Erosion Kernel Size', 'controls', 1, 20, lambda x: x)
    cv2.createTrackbar('Erosion Iteration', 'controls', 1, 10, lambda x: x)
    cv2.createTrackbar('Dilation Kernel Size', 'controls', 1, 20, lambda x: x)
    cv2.createTrackbar('Dilation Iteration', 'controls', 1, 10, lambda x: x)
    cv2.createTrackbar('Threshold Flag', 'controls', 2, 5, lambda x: x)
    cv2.createTrackbar('BITWISE ON OFF', 'controls', 0, 1, lambda x: x)
    cv2.createTrackbar('ADAPTIVE TH', 'controls', 0, 1, lambda x: x)
    cv2.createTrackbar('REMOVE LINES', 'controls', 0, 1, lambda x: x)

    def th_key_maker(key):
        if key == 1:
            # print("cv2.THRESH_BINARY_INV")
            return cv2.THRESH_BINARY_INV
        elif key == 2:
            # print("cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU")
            return cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        elif key == 3:
            # print("cv2.THRESH_TOZERO")
            return cv2.THRESH_TOZERO
        elif key == 4:
            # print("cv2.THRESH_TOZERO_INV")
            return cv2.THRESH_TOZERO_INV
        elif key == 5:
            # print("cv2.THRESH_TRUNC")
            return cv2.THRESH_TRUNC
        else:
            # print("cv2.THRESH_BINARY")
            return cv2.THRESH_BINARY

    while True:
        blur = int(cv2.getTrackbarPos('Blur', 'controls'))
        blur_it = int(cv2.getTrackbarPos('Blur Iteration', 'controls'))
        th1 = int(cv2.getTrackbarPos('Threshold Block Size', 'controls'))
        th2 = int(cv2.getTrackbarPos('Threshold Constant', 'controls'))
        eksize = int(cv2.getTrackbarPos('Erosion Kernel Size', 'controls'))
        eit = int(cv2.getTrackbarPos('Erosion Iteration', 'controls'))
        dksize = int(cv2.getTrackbarPos('Dilation Kernel Size', 'controls'))
        dit = int(cv2.getTrackbarPos('Dilation Iteration', 'controls'))
        th_key_num = int(cv2.getTrackbarPos('Threshold Flag', 'controls'))
        bitwise_on_off = int(cv2.getTrackbarPos('BITWISE ON OFF', 'controls'))
        adaptive_to_normal = int(cv2.getTrackbarPos('ADAPTIVE TH', 'controls'))

        th_key = th_key_maker(th_key_num)

        while blur % 2 == 0 or blur < 3:
            blur += 1
        while th1 % 2 == 0 or th1 < 2:
            th1 += 1
        while th2 % 2 == 0:
            th2 += 1

        # blurred = cv2.medianBlur(img,blur)
        blurred = cv2.GaussianBlur(img, (blur, blur), blur_it)
        # blurred = cv2.GaussianBlur(img, (blur, blur), blur_it)

        if adaptive_to_normal:
            threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, th1, th2)
        else:
            qret, threshold = cv2.threshold(blurred, th1, th2, th_key)
            # ret, threshold = cv2.threshold(blurred, th1, th2, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        if bitwise_on_off:
            bitwise = cv2.bitwise_not(threshold)
        else:
            bitwise = threshold

        erosion = cv2.erode(bitwise, (eksize, eksize), eit)
        dilate = cv2.dilate(erosion, (dksize, dksize), dit)
        cv2.imshow("showup", dilate)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # print("dataset" + str(counter) + ".png saving")
            print("OCR READING STARTING")
            #
            cv2.imwrite("C:/Users/ozcan/Desktop/crop_baba.jpg", dilate)
            pytesseract_func(dilate)
            print("##########################################################################################")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def pytesseract_func(img):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)

    text = ""
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img)
    for i in range(0, len(result)):
        text += result[i][1] + ' '
        ##easyocr matrix kodu

    print(f'Licence Plate: {text}')


img = cv2.imread("cropped/7.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
goruntuisleme(img)
