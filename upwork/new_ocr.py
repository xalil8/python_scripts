
import cv2
import pytesseract
import easyocr

def pytesseract_func():
    img = cv2.imread("ocr_example.jpg",1)
    cv2.namedWindow("My_window",cv2.WINDOW_NORMAL)
    #print("calıştı")
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    reader = easyocr.Reader(['en'])
    text1 = reader.readtext(img)
    """print(text)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--EASYOCR--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")"""
    new_list = []
    """for i in range(5,len(text1)-1):
        if (i%3) == 2:
            new_list.append(text1[i][1])
    
    print(new_list)"""
    print("\n"*10)
    for i in range(len(text1)):
        if text1[i][0][1][0] < 580:
            print(text1[i][1],"accuracy =", text1[i][2])
            #print(text1[i])
            img = cv2.rectangle(img,tuple(text1[i][0][0]), tuple(text1[i][0][2]), (0, 255, 0), 6)

    cv2.imshow("My_window", img)
    cv2.waitKey(0)

pytesseract_func()