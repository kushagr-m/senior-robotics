from imutils.video import VideoStream
import imutils
import numpy as np
import cv2 as cv
from time import sleep
import os

cvDebugLevel = 0 # show a cv.imshow output as well as debugging windows (not required for play, disable)
frameDimensions = 320,240

#if os.name == "posix" and os.environ['DISPLAY']:
    # Running in a headless session
    #cvDebugLevel = 0

ballCenter = None

def getCamera(camera=1):
    print("Getting camera")
    
    vs = VideoStream(src=camera).start() # initialise using webcam video camera
    print("Trying to use Webcam")
    sleep(0.1)
    try:
        vs.read().any()
        print("Webcam Success")
    except:
        vs = VideoStream(usePiCamera=1>0).start() # initialise using picamera
        print("Webcam Failed\nUsing PiCamera")

    sleep(2.0) # give sensor time to warm up

    return vs
vs = getCamera()

def getFrame():
    frame = vs.read() # read the frame
    frame = imutils.resize(frame, frameDimensions[0]) # resize the frame
    return frame

def adjustGamma(image, gamma=1.0):
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv.LUT(image, table)

def cleanup():
    print("Doing Cleanup")
    cv.destroyAllWindows()
    vs.stop()

def getBallCenter():
    global ballCenter
    if ballCenter is not None:
        ballX = int(ballCenter[0]-(frameDimensions[0]/2))
        ballY = int(ballCenter[1]-(frameDimensions[1]/2))
        return ballX, ballY
    else:
        return None

def loop():
    global ballCenter

    rgb = getFrame()

    # convert to HSV before blurring to reduce RGB interference in HSV
    hsv = cv.cvtColor(rgb, cv.COLOR_BGR2HSV)

    # splitting to make it easier to use each channel
    hsvHue,hsvSat,hsvVal = cv.split(hsv)
    rgbBlue,rgbGreen,rgbRed = cv.split(rgb)
    
    # removing the blue channel from the red channel leaves the ROUGH location of the ball
    ballRemoveBG = cv.add(rgbBlue,rgbGreen)
    ballGrayscale = cv.subtract(rgbRed,ballRemoveBG)
    
    # getting the maximum brightness to inRange, using hsvSat as a floor
    hsvSatMask = cv.inRange(hsvSat,25,255)
    maxVal = cv.minMaxLoc(ballGrayscale, hsvSatMask)[1]
    
    # creating a 2-bit image using hsvHue to use as a mask for the ball
    hsvHueMask = cv.inRange(hsvHue,0,50)
    
    # if maxVal < 80, most likely that the ball isn't even in frame
    if maxVal >= 80:

        ballMask = cv.inRange(ballGrayscale, (maxVal-40), 255) # converting to a BW mask
        ballMask = cv.bitwise_and(ballMask,hsvHueMask) # using bitwise_and to mask

        # dilate to fill gaps when ball is partially obscured
        # rectangle is much quicker than ellipse, ballCenter remains similar
        ballMask = cv.dilate(ballMask,cv.getStructuringElement(cv.MORPH_RECT,(13,13)))

        # get the center of the mask with moments
        moments = cv.moments(ballMask)

        mDenom = moments["m00"]
        if mDenom == 0:
            mDenom = 1 # weird bug: near the edges of the frame, moments["m00"] = 0, throwing a d0 error
        ballCenter = int(moments["m10"] / mDenom), int(moments["m01"] / mDenom)	
        
    else:
        ballMask = cv.inRange(ballGrayscale, 255, 255) # blank screen
        ballCenter = None

    print("ballCenter =", ballCenter)
    
    if cvDebugLevel >= 1: #cvDebug outputs

        ballMaskRGB = cv.cvtColor(ballMask, cv.COLOR_GRAY2BGR) # convert 2bit ballMask to BGR to draw colours on it
        
        ballMask, ballOutline, hierarchy = cv.findContours(ballMask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE) # get the outline of ballMask
        cv.drawContours(rgb, ballOutline, -1, (0,255,0), 3) # draw outline of ball (0,255,0)
        cv.circle(rgb, ballCenter, 3, (255,0,0), -1) # draw dot at ballCenter (255,0,0)

        cv.imshow("Output", rgb)

        if cvDebugLevel >= 2:
            cv.imshow("RGB Red", rgbRed)
            cv.imshow("RGB Green", rgbGreen)
            cv.imshow("RGB Blue", rgbBlue)
            cv.imshow("Ball Gray", ballGrayscale)
            
            cv.imshow("Processed HSV", hsv)
            cv.imshow("HSV Hue", hsvHue)
            cv.imshow("HSV Saturation", hsvSatMask)
            cv.imshow("HSV Value", hsvVal)
            
            cv.circle(ballMaskRGB, ballCenter, 5, (0,0,255), -1) # draw red dot on ball mask at ballCenter		
            cv.imshow("ball mask", ballMaskRGB)

        if cv.waitKey(1) & 0xFF == ord('q'):
            return True
