import cv2
import numpy as np

goalCalibration = True

mins = [0,0,0]
maxs = [0,0,0]

video = cv2.VideoCapture(1)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

def trackbarCallback(value, data):
    pass

cv2.createTrackbar('Hmin', 'image', 0, 255, trackbarCallback)
cv2.createTrackbar('Smin', 'image', 0, 255, trackbarCallback)
cv2.createTrackbar('Vmin', 'image', 0, 255, trackbarCallback)

cv2.createTrackbar('Hmax', 'image', 0, 255, trackbarCallback)
cv2.createTrackbar('Smax', 'image', 0, 255, trackbarCallback)
cv2.createTrackbar('Vmax', 'image', 0, 255, trackbarCallback)

while(True):
    (grabbed, frame) = video.read()

    if goalCalibration:
        frame = cv2.imread('./../callibyellow.png')

    if grabbed:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

        hmin = cv2.getTrackbarPos('Hmin', 'image')
        smin = cv2.getTrackbarPos('Smin', 'image')
        vmin = cv2.getTrackbarPos('Vmin', 'image')

        hmax = cv2.getTrackbarPos('Hmax', 'image')
        smax = cv2.getTrackbarPos('Smax', 'image')
        vmax = cv2.getTrackbarPos('Vmax', 'image')

        lower = (hmin,smin,vmin)
        upper = (hmax,smax,vmax)
        
        mask = cv2.inRange(hsv, lower, upper)
        cv2.imshow('image', mask)
        cv2.imshow('original', frame)

    key = cv2.waitKey(10)
    if key == 27:
        break

cv2.destroyAllWindows()