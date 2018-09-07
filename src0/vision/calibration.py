import cv2
import numpy as np
import os
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

goalCalibration = False

mins = [0,0,0]
maxs = [0,0,0]

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('original', cv2.WINDOW_NORMAL)

def trackbarCallback(value):
    pass

cv2.createTrackbar('GoalCalibration', 'image', 0, 1, trackbarCallback)

cv2.createTrackbar('Hmin', 'image', 0, 255, trackbarCallback)
cv2.createTrackbar('Smin', 'image', 0, 255, trackbarCallback)
cv2.createTrackbar('Vmin', 'image', 0, 255, trackbarCallback)

cv2.createTrackbar('Hmax', 'image', 0, 255, trackbarCallback)
cv2.createTrackbar('Smax', 'image', 0, 255, trackbarCallback)
cv2.createTrackbar('Vmax', 'image', 0, 255, trackbarCallback)

cv2.createTrackbar('gamma', 'image', 0, 350, trackbarCallback)

cv2.setTrackbarPos('Hmin', 'image', 0)
cv2.setTrackbarPos('Hmax', 'image', 255)
cv2.setTrackbarPos('Smin', 'image', 0)
cv2.setTrackbarPos('Smax', 'image', 255)
cv2.setTrackbarPos('Vmin', 'image', 0)
cv2.setTrackbarPos('Vmax', 'image', 255)

autocalibration_tolerance = 30
def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONUP:
        raw = PiRGBArray(camera, size=(640, 480))
        camera.capture(raw, format="bgr")
        frame = raw.array

        goalCalibration = cv2.getTrackbarPos('GoalCalibration', 'image') == 1
        if goalCalibration:
            frame = cv2.imread(os.path.dirname(os.path.abspath(__file__)) + '/../../callibyellow.png')

        frame = cv2.resize(frame, (320, 240))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        data = hsv[y, x]

        cv2.setTrackbarPos('Hmin', 'image', data[0] - autocalibration_tolerance)
        cv2.setTrackbarPos('Hmax', 'image', data[0] + autocalibration_tolerance)
        cv2.setTrackbarPos('Smin', 'image', data[1] - autocalibration_tolerance)
        cv2.setTrackbarPos('Smax', 'image', data[1] + autocalibration_tolerance)
        cv2.setTrackbarPos('Vmin', 'image', data[2] - autocalibration_tolerance)
        cv2.setTrackbarPos('Vmax', 'image', data[2] + autocalibration_tolerance)
# cv2.setMouseCallback('original', onMouse)

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")

	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

for _frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = _frame.array

    goalCalibration = cv2.getTrackbarPos('GoalCalibration', 'image') == 1
    if goalCalibration:
        frame = cv2.imread(os.path.dirname(os.path.abspath(__file__)) + '/../../callibyellow.png')

    gamma = cv2.getTrackbarPos('gamma', 'image') / 100
    if gamma == 0:
        gamma = 0.1

    frame = adjust_gamma(frame, gamma)

    hsv = cv2.resize(frame, (320, 240))
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 5)

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

    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == 115:
        hmin = cv2.getTrackbarPos('Hmin', 'image')
        smin = cv2.getTrackbarPos('Smin', 'image')
        vmin = cv2.getTrackbarPos('Vmin', 'image')

        hmax = cv2.getTrackbarPos('Hmax', 'image')
        smax = cv2.getTrackbarPos('Smax', 'image')
        vmax = cv2.getTrackbarPos('Vmax', 'image')

        settingsFileRead = open(os.path.dirname(os.path.abspath(__file__)) + "/../calibrationSettings.py")
        lines = []
      
        for line in settingsFileRead:
            key = line.split(" = ")[0]
            
            if goalCalibration:
                if key == "goalLower":
                    line = key + " = (" + str(hmin) + ", " + str(smin) + ", " + str(vmin) + ")\n" 
                elif key == "goalUpper":
                    line = key + " = (" + str(hmax) + ", " + str(smax) + ", " + str(vmax) + ")\n"
                elif key == "goalWidthHeightRatio":
                    mask = cv2.inRange(hsv, (hmin, smin, vmin), (hmax, smax, vmax))
                    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    c = max(contours, key=cv2.contourArea)
                    perimeter = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
                    (x, y, w, h) = cv2.boundingRect(approx)
                    line = key + " = " + str(round(w / h, 2)) + "\n"
            else:
                if key == "ballLower":
                    line = key + " = (" + str(hmin) + ", " + str(smin) + ", " + str(vmin) + ")\n" 
                elif key == "ballUpper":
                    line = key + " = (" + str(hmax) + ", " + str(smax) + ", " + str(vmax) + ")\n" 
            
            lines.append(line)

        settingsFileRead.close()

        settingsFileWrite = open(os.path.dirname(os.path.abspath(__file__)) + "/../calibrationSettings.py", "w")
        settingsFileWrite.writelines(lines)
        settingsFileWrite.close()

    rawCapture.truncate(0)

cv2.destroyAllWindows()