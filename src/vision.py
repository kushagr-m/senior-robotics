from imutils.video import VideoStream
import imutils
import numpy as np
import cv2 as cv
import time
import os
import math as maths
import collections

cvDebugLevel = 2 # show a cv.imshow output as well as debugging windows (not required for play, disable)
frameDimensions = 320,240

rotateFrame = True
ballCenter = None

queueLength = 32

ballQueue = collections.deque(maxlen=queueLength)
maxValQueue = collections.deque(maxlen=queueLength)

frameCount = 0
fpsTime = time.perf_counter()
fps = 0

if os.name == "posix" and os.getenv("DISPLAY") is None:
    # Running in a headless session
    cvDebugLevel = 0

def getCamera():
	global rotateFrame
	rotateFrame = False
	print("VISION: Initialising Camera...")

	for i in [1,0]:
		print("VISION: Trying webcam ",i,"...",sep="")
		vs = VideoStream(src=i).start()
		time.sleep(0.1)
		try:
			vs.read().any()
			rotateFrame = False
			print("VISION: Webcam",i,"successful.")
			return vs

		except:
			print("VISION: Webcam",i,"failed.")

	print("VISION: Trying PiCamera...")
	try:
		vs = VideoStream(usePiCamera=1>0).start()
		print("VISION: PiCamera successful.")
		rotateFrame = True
		time.sleep(2.0)
	except:
		print("VISION: PiCamera Failed.")
		return False

vs = getCamera()
if vs is False:
	print("VISION: Unable to initialise camera. Exiting...")
	exit()

def getFrame():
    frame = vs.read() # read the frame
    frame = imutils.resize(frame, frameDimensions[0]) # resize the frame
    frame = cv.GaussianBlur(frame, (15,15),0)
    if rotateFrame: 
        frame = imutils.rotate(frame, 180)
    return frame

def adjustGamma(image, gamma=1.0):
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv.LUT(image, table)

def dist(A,B):
	x = A[0]
	y = A[1]
	a = B[0]
	b = B[1]
	dist = maths.sqrt(((x-a)**2)+((y-b)**2))
	return dist

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
    #queues
    global ballQueue
    global maxValQueue
    global frameCount
    global fpsTime
    global fps

    rgb = getFrame()

    hsv = cv.cvtColor(rgb, cv.COLOR_BGR2HSV)
    hsvHue,hsvSat,hsvVal = cv.split(hsv)
    rgbBlue,rgbGreen,rgbRed = cv.split(rgb)
    
    # removing the blue channel from the red channel leaves the ROUGH location of the ball
    
    ballGrayscale = cv.subtract(rgbRed,rgbBlue)
    ballGrayscale = cv.subtract(ballGrayscale,rgbGreen)
    
    # getting the maximum brightness to inRange, using hsvSat as a floor
    hsvSatMask = cv.inRange(hsvSat,25,255)
    maxVal = cv.minMaxLoc(ballGrayscale, hsvSatMask)[1]
    
    # creating a mask for the ball
    hsvHueMask = cv.inRange(hsvHue,0,25)
    
    # if maxVal < 70, most likely that the ball isn't even in frame
    if maxVal >= 75:
        ballMask = cv.inRange(ballGrayscale, (maxVal-40), 255) # converting to a BW mask
        ballMask = cv.bitwise_and(ballMask,hsvHueMask) # using bitwise_and to mask

        # dilate to fill gaps when ball is partially obscured
        ballMask = cv.dilate(ballMask,cv.getStructuringElement(cv.MORPH_ELLIPSE,(19,19)))

        # get the center of the mask with moments
        moments = cv.moments(ballMask)

        mDenom = moments["m00"]
        if mDenom == 0:
            mDenom = 1 # weird bug: near the edges of the frame, moments["m00"] = 0, throwing a d0 error
        ballCenter = int(moments["m10"] / mDenom), int(moments["m01"] / mDenom)	
        
    else:
        ballMask = cv.inRange(ballGrayscale, 255, 255) # blank screen
        ballCenter = None

    #get circles and shit
    ballMask, ballOutline, hierarchy = cv.findContours(ballMask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE) # get the outline of ballMask
    
    yellowGoal = False
    outlineCenter,outlineRadius = (0,0),0
    strX,strY,strW,strH = None,None,None,None
    
    if ballOutline is not None:
        try:
            outlineCenter,outlineRadius = cv.minEnclosingCircle(ballOutline[0])
            outlineCenter = int(outlineCenter[0]),int(outlineCenter[1])
            outlineRadius = int(outlineRadius)

            if dist(ballCenter,outlineCenter)>=(2*outlineRadius/3):
                yellowGoal = True
        except:
            pass

        try:
            strX,strY,strW,strH = cv.boundingRect(ballOutline[0])
            outlineRect = cv.minAreaRect(ballOutline[0])
            outlineBox = np.int0(cv.boxPoints(outlineRect))

            if (outlineRadius/strH)>1:
                yellowGoal = True

            if strW/strH>=1.5:
                yellowGoal = True

            if strH < outlineRadius * 1.5 or strW < outlineRadius * 1.5:
                yellowGoal = True

        except:
            outlineBox = None


    if yellowGoal is True:
        outlineCenter,outlineRadius = (0,0),0
        strX,strY,strW,strH = None,None,None,None
        ballCenter = None

    
    #queueing
    ballQueue.append(ballCenter)
    maxValQueue.append(maxVal)

    if cvDebugLevel >= 1: #cvDebug outputs

        ballMaskRGB = cv.cvtColor(ballMask, cv.COLOR_GRAY2BGR) # convert 2bit ballMask to BGR to draw colours on it

        cv.drawContours(rgb, ballOutline, -1, (0,255,0), 3) # draw outline of ball (0,255,0)
        cv.circle(rgb, outlineCenter, outlineRadius, (125,255,125), 3)

        if outlineBox is not None: cv.drawContours(ballMaskRGB, [outlineBox],0,(0,0,255),2)
        if strX: cv.rectangle(ballMaskRGB,(strX,strY),(strX+strW,strY+strH),(255,200,0),2)
        cv.circle(ballMaskRGB, outlineCenter, outlineRadius, (0,255,0), 3)

        for i in ballQueue:
            cv.circle(rgb, i, 4, (255,0,0), -1) # draw dot at ballCenter (255,0,0)
            cv.circle(ballMaskRGB, i, 2, (0,0,255), -1) # draw red dot on ball mask at ballCenter	

        cv.circle(ballMaskRGB, ballCenter, 4, (0,0,255), -1)	
            

        if ballCenter is not None: cv.putText(ballMaskRGB, str(getBallCenter()),(int(ballCenter[0]+(outlineRadius/90)),int(ballCenter[1]+(outlineRadius/40))),cv.FONT_HERSHEY_PLAIN,(outlineRadius/40)+0.3,(125,125,125),int((outlineRadius/30)+0.3))

        cv.imshow("Output", rgb)

        if cvDebugLevel >= 2:
            cv.imshow("RGB Red", rgbRed)
            cv.imshow("RGB Green", rgbGreen)
            cv.imshow("RGB Blue", rgbBlue)
            cv.imshow("Ball Gray", ballGrayscale)
            
            cv.imshow("Processed HSV", hsv)
            cv.imshow("HSV Hue", hsvHue)
            cv.imshow("HSV Saturation", hsvSat)
            cv.imshow("HSV Value", hsvVal)
            
            cv.imshow("ball mask", ballMaskRGB)

        if cv.waitKey(1) & 0xFF == ord('q'):
            return True

    # Update FPS stats
    frameCount = frameCount + 1
    if frameCount % 30 == 0:
        # Recalculate fps every 30 frames
        currentTime = time.perf_counter()
        fps = maths.floor(30 / (currentTime - fpsTime))
        fpsTime = currentTime

    print("ballCenter =", ballCenter, "maxValue  =", int(maxVal), "fps       =", fps)

if __name__ == '__main__':
    while True:
        ex = loop()
        if ex: break
