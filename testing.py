#most importantly for this code to run is to import OpenCV which we do in the below line
from imutils.perspective import four_point_transform
import cv2
import numpy as np
import threading

def get_red():
        mask = cv2.inRange(img_hsv, lower_red, upper_red) # Masking the image to find our color
        mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 200:
                        cv2.putText(img, "STOP", (cx + 200, cy + 230), 0, 1, (255, 255, 255), 4)
                        x, y, w, h = cv2.boundingRect(mask_contour)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3) # Drawing rectangle
def get_orange():
    mask = cv2.inRange(img_hsv, lower_orange, upper_orange) # Masking the image to find our color
    mask_contours2, hierarchy2 = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
    if len(mask_contours2) != 0:
        for mask_contour in mask_contours2:
            if cv2.contourArea(mask_contour) > 200:
                    cv2.putText(img, "STOP", (cx + 200, cy + 230), 0, 1, (255, 255, 255), 4)
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3) # Drawing rectangle

def get_green():
    mask2 = cv2.inRange(img_hsv, lower_green, upper_green)
    mask_contours3, hierarchy3 = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
    
    if len(mask_contours3) != 0:
        for mask_contour in mask_contours3:
            if cv2.contourArea(mask_contour) > 150:
                cv2.putText(img, "GO", (cx + 200, cy + 230), 0, 1, (255, 255, 255), 4)
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3) # Drawing rectangle

# set up camera object called Cap which we will use to find OpenCV
cap = cv2.VideoCapture(0)

lower_red = np.array([3, 60, 60])
upper_red = np.array([5, 255, 255])     # (These rangers will detect Red)
lower_orange = np.array([5, 100, 150])
upper_orange = np.array([88, 225, 225]) # (These ranges will detect Orange)
lower_green = np.array([13, 59, 10])
upper_green = np.array([50, 255, 255])  # (These ranges will detect Green)
    
#This creates an Infinite loop to keep your camera searching for data at all times
while True:
    _, img = cap.read()
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format
    height, width, _ = img.shape
    cx = int(width / 2)
    cy = int(height / 2)  

    # Below is the method to read the QR code by detetecting the bounding box coords and decoding the hidden QR data 
    # QR code detection Method
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    
    # This is how we get that Blue Box around our Data. This will draw one, and then Write the Data along with the top (Alter the numbers here to change the colour and thickness of the text)
    if(data and bbox is not None):
        print(data)
        print(np.int32(bbox))
        index_point = np.int32(bbox)

        rect = four_point_transform(img, index_point.reshape(4, 2))
        
        thread1 = threading.Thread(target=get_red())
        thread2 = threading.Thread(target=get_orange())
        thread3 = threading.Thread(target=get_green())
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()

    cv2.imshow("img", img)
    if cv2.waitKey(1) == ord("q"):
        cap.close()
        cv2.destroyAllWindows()
        break
