import time
import cv2
import mss
import numpy as np

def nothing(x):
    pass


cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of 
# H,S and V channels. The Arguments are like this: Name of trackbar, 
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


def monitor():
    monitor_number = 2
    with mss.mss() as sct:
        # Part of the screen to capture
        mon = sct.monitors[monitor_number]
        monitor = {"top": mon["top"] + 0, "left": mon["left"] +0, "width": 1920, "height": 1080,"mon": monitor_number}

        while "Screen capturing":
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            img = np.array(sct.grab(monitor))
           

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            l_h = cv2.getTrackbarPos("L - H", "Trackbars")
            l_s = cv2.getTrackbarPos("L - S", "Trackbars")
            l_v = cv2.getTrackbarPos("L - V", "Trackbars")
            u_h = cv2.getTrackbarPos("U - H", "Trackbars")
            u_s = cv2.getTrackbarPos("U - S", "Trackbars")
            u_v = cv2.getTrackbarPos("U - V", "Trackbars")

            lower_range = np.array([l_h, l_s, l_v])
            upper_range = np.array([u_h, u_s, u_v])

            # Filter the image and get the binary mask, where white represents 
            # your target color
            mask = cv2.inRange(hsv, lower_range, upper_range)

            # You can also visualize the real part of the target color (Optional)
            res = cv2.bitwise_and(img, img, mask=mask)

            # Converting the binary mask to 3 channel image, this is just so 
            # we can stack it with the others
            mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGBA)
            #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            # stack the mask, orginal frame and the filtered result
            stacked = np.hstack((mask_3,img,res))






            # Display the picture
            #cv2.imshow("OpenCV/Numpy normal", img)
        # cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))
            cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.35,fy=0.35))

            # Display the picture in grayscale
            # cv2.imshow('OpenCV/Numpy grayscale',
            #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

            #print("fps: {}".format(1 / (time.time() - last_time)))

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

def webcam():
    cap = cv2.VideoCapture(0)
    cap.set(2,1920)
    cap.set(3,1080)
    while True:
    
        # Start reading the webcam feed frame by frame.
        ret, frame = cap.read()
        if not ret:
            break
        # Flip the frame horizontally (Not required)
        frame = cv2.flip( frame, 1 ) 
        
        # Convert the BGR image to HSV image.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get the new values of the trackbar in real time as the user changes 
        # them
        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
        # Set the lower and upper HSV range according to the value selected
        # by the trackbar
        lower_range = np.array([l_h, l_s, l_v])
        upper_range = np.array([u_h, u_s, u_v])
        
        # Filter the image and get the binary mask, where white represents 
        # your target color
        mask = cv2.inRange(hsv, lower_range, upper_range)
    
        # You can also visualize the real part of the target color (Optional)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Converting the binary mask to 3 channel image, this is just so 
        # we can stack it with the others
        mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        # stack the mask, orginal frame and the filtered result
        stacked = np.hstack((mask_3,frame,res))
        
        # Show this stacked frame at 40% of the size.
        cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))
        
        # If the user presses ESC then exit the program
        key = cv2.waitKey(1)
        if key == 27:
            break
        
        # If the user presses `s` then print this array.
        if key == ord('s'):
            
            thearray = [[l_h,l_s,l_v],[u_h, u_s, u_v]]
            print(thearray)
            
            # Also save this array as penval.npy
            np.save('hsv_value',thearray)
            break
        
    # Release the camera & destroy the windows.    
    cap.release()
    cv2.destroyAllWindows()

#monitor()
#webcam()