import time

#https://www.geeksforgeeks.org/count-number-of-object-using-python-opencv/
#https://stackoverflow.com/questions/44588279/find-and-draw-the-largest-contour-in-opencv-on-a-specific-color-python

import cv2
from matplotlib.pyplot import draw
import mss
import numpy

monitor_number = 2


with mss.mss() as sct:
    # Part of the screen to capture
    mon = sct.monitors[monitor_number]
    monitor = {"top": mon["top"] + 0, "left": mon["left"] +0, "width": 1920, "height": 1080,"mon": monitor_number}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_range = (0,0,0)
        upper_range = (179,255,0)

        mask = cv2.inRange(hsv, lower_range, upper_range)

        
        blur = cv2.GaussianBlur(mask, (5, 5), 0)
        #canny = cv2.Canny(blur, 30, 150, 3)
        #dilated = cv2.dilate(canny, (1, 1), iterations=0)
        
        # (cnt, hierarchy) = cv2.findContours(
        #     blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

        contours,hierarchy = cv2.findContours(blur, 1, 2)
        #drawing = cv2.drawContours(img , contours, -1, (255,0,0), 5)

        # find the biggest countour (c) by the area
        if len(contours) != 0:
            c = max(contours, key = cv2.contourArea)
            drawing = cv2.polylines(img,[c],True,(255,255,50))




        
        #print("Planes in the image : ", len(cnt))

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", drawing) #mask

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        #print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break