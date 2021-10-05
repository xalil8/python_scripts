
import cv2
import pytesseract
import easyocr

def pytesseract_func(img):
    print("calıştı")
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    reader = easyocr.Reader(['en'])
    text1 = reader.readtext(img)
    print(text)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--EASYOCR--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(text1)


def goruntuisleme():
    print("lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")



   # img = cv2.imread("ocr_example.jpg")

    img = cv2.imread("berkplaka.png")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


    #cv2.namedWindow('line', cv2.WINDOW_NORMAL)
    cv2.namedWindow("showup",cv2.WINDOW_NORMAL)
    cv2.namedWindow('controls',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('controls',850,250)
    cv2.resizeWindow('showup',850,250)



    cv2.createTrackbar('Blur','controls',0,20,lambda x:x)
    cv2.createTrackbar('Blur Iteration','controls',0,10,lambda x:x)
    cv2.createTrackbar('Threshold Block Size','controls', 222, 255, lambda x:x)
    cv2.createTrackbar('Threshold Constant','controls', 20, 255, lambda x:x)
    cv2.createTrackbar('Erosion Kernel Size','controls', 1, 20, lambda x:x)
    cv2.createTrackbar('Erosion Iteration','controls',1, 10, lambda x:x)
    cv2.createTrackbar('Dilation Kernel Size','controls', 1, 20, lambda x:x)
    cv2.createTrackbar('Dilation Iteration','controls', 1, 10, lambda x:x)
    cv2.createTrackbar('Threshold Flag','controls', 2, 5, lambda x:x)
    cv2.createTrackbar('BITWISE ON OFF','controls', 0, 1, lambda x:x)
    cv2.createTrackbar('ADAPTIVE TH','controls', 0, 1, lambda x:x)
    cv2.createTrackbar('REMOVE LINES','controls', 0, 1, lambda x:x)



    def th_key_maker(key):

        if key == 1:
            #print("cv2.THRESH_BINARY_INV")
            return cv2.THRESH_BINARY_INV
        elif key == 2:
            #print("cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU")
            return cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
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

    counter = 2

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
        #line_remover =int(cv2.getTrackbarPos('REMOVE LINES', 'controls'))




        th_key = th_key_maker(th_key_num)


        while blur % 2 == 0 or blur <3:
            blur += 1

        while th1 % 2 == 0 or th1 < 2:
            th1 += 1

        while th2 % 2 == 0:
            th2 += 1

        #blurred = cv2.medianBlur(img,blur)
        blurred = cv2.GaussianBlur(img, (blur, blur), blur_it)
        #blurred = cv2.GaussianBlur(img, (blur, blur), blur_it)

        if adaptive_to_normal:

            threshold = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,th1,th2)
        else:
            qret, threshold = cv2.threshold(blurred, th1, th2, th_key)
            #ret, threshold = cv2.threshold(blurred, th1, th2, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)



        if bitwise_on_off:
            bitwise = cv2.bitwise_not(threshold)
        else:
            bitwise = threshold


        erosion = cv2.erode(bitwise, (eksize,eksize), eit)
        dilate = cv2.dilate(erosion,(dksize, dksize), dit)

        """if line_remover:
            removed_line = line_remover_func(dilate, img)[0]
            actual_image = line_remover_func(dilate, img)[1]
        else:
            removed_line = dilate
            actual_image = img"""


        cv2.imshow("showup", dilate)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            #print("dataset" + str(counter) + ".png saving")
            print("OCR READING STARTING")
            pytesseract_func(dilate)
            print("##########################################################################################")
            #tifffile.imwrite("C:/Users/ozcan/Desktop/dataset-tiff/testlan.gorton.exp" + str(counter) + ".tiff", dilate)
            #cv2.imwrite("C:/Users/ozcan/Desktop/upwork_ocr/eng.gorton.exp" + str(counter) + ".png", threshold)
            #cv2.imwrite("C:/Users/ozcan/Desktop/letter_dataset/letter" + str(counter) + ".png", dilate)


            counter = counter + 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()




def line_remover_func(img):
    img_real = img.copy()
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
    cv2.namedWindow("detected_lines",cv2.WINDOW_NORMAL)
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(img, [c], -1, (255, 255, 255), 2)

    # Repair image
    repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 6))
    result = 255 - cv2.morphologyEx(255 - img, cv2.MORPH_CLOSE, repair_kernel, iterations=1)

    cv2.imshow('thresh', thresh)
    cv2.imshow('detected_lines', detected_lines)
    cv2.imshow('image', img_real)
    cv2.imshow('result', result)
    cv2.waitKey()


img = cv2.imread("tresh.png")

#line_remover_func(img)
#print("code done ")

goruntuisleme()





