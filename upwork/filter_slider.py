import cv2

#import numpy as np
import easyocr


def oku(img):
    print("OCR GONNA START BABAA")

    text = ""
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img)
    for i in range(0, len(result)):
        text += result[i][1] + ' '
        ##easyocr matrix kodu

    print(f'Licence Plate: {text}')


def baba_filtre(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (77, 77))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)

    oku(blackhat)
    cv2.namedWindow("babaa",cv2.WINDOW_NORMAL)
    cv2.imshow("babaa", blackhat)

    cv2.waitKey(0)




img = cv2.imread("cropped/1.jpg")

baba_filtre(img)
