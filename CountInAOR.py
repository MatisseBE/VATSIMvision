"AOR = Area of Responsibility"
#https://realpython.com/python-opencv-color-spaces/
#https://stackoverflow.com/questions/50783619/getting-the-x-and-y-coordinates-from-cv2-contour-in-open-cv-python-and-store-it
#https://www.geeksforgeeks.org/python-opencv-cv2-polylines-method/
#https://stackoverflow.com/questions/44588279/find-and-draw-the-largest-contour-in-opencv-on-a-specific-color-python
#https://stackoverflow.com/questions/36311398/contour-shows-dots-rather-than-a-curve-when-retrieving-it-from-the-list-but-sho
#https://python-mss.readthedocs.io/examples.html?highlight=monitor#part-of-the-screen-of-the-2nd-monitor
#https://www.geeksforgeeks.org/count-number-of-object-using-python-opencv/
#https://stackoverflow.com/questions/44588279/find-and-draw-the-largest-contour-in-opencv-on-a-specific-color-python

import time
import cv2
import mss
import numpy

monitor_number = 2


with mss.mss() as sct:
    # Part of the screen to capture
    mon = sct.monitors[monitor_number]
    monitor = {"top": mon["top"] + 0, "left": mon["left"] + 0, "width": 1920, "height": 1080,"mon": monitor_number}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        canvas = numpy.array(sct.grab(monitor))

        hsv = cv2.cvtColor(canvas, cv2.COLOR_BGR2HSV)

        #AOR
        lower_range_AOR = (0,0,0)
        upper_range_AOR = (179,255,0)

        mask_AOR = cv2.inRange(hsv, lower_range_AOR, upper_range_AOR)    #Masks what we look for (the aor)    
        blur_AOR = cv2.GaussianBlur(mask_AOR, (5, 5), 0)                 #Adds blur for globality

        contours,hierarchy = cv2.findContours(blur_AOR, 1, 2)            #Get all contours that may be AOR

        if len(contours) != 0:
            AOR = max(contours, key = cv2.contourArea)                   #Largest contour is AOR
            drawing = cv2.polylines(canvas,[AOR],True,(255,255,50))      #Draw AOR

        

        #Planes
        lower_range_plane = (110,124,255)
        upper_range_plane = (130,165,255)

        mask_plane = cv2.inRange(hsv, lower_range_plane, upper_range_plane)
        blur_plane = cv2.GaussianBlur(mask_plane, (5, 5), 0)

        contours,hierarchy = cv2.findContours(blur_plane, 1, 2)

        planes = 0
        if len(contours) != 0 :
                #For each found plane
                for i in range(len(contours)):
                    c = contours[i]                                                             #Get contour

                    coors = []                                                                  #List of XY coordiantes of plane's contour
                    for position in c:
                        [(x,y)] = position
                        coors.append((int(x),int(y)))

                    #For each coordinate of the contour of the plane
                    for coor in coors:
                        dist = cv2.pointPolygonTest(AOR,coor,True)                              #Positive distance means coordinate inside AOR
                        if dist > 0:
                            planes += 1
                            drawing = cv2.drawContours(drawing , contours, i, (0,255,0), 0)     #bgr - draw countour
                            drawing = cv2.putText(drawing,str(i), (coor), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,200,200))
                            break


        print("Planes in the image : ", planes)
        
        # Display the picture
        cv2.imshow("Matisse's plane counter", drawing)                                          #mask_AOR
        #print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break