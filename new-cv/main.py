from imutils.video import VideoStream
import imutils
import numpy as np
import cv2 as cv
from time import sleep

debug = True

frameDimensions = 320,240

medBlurVal = 13
gaussVal = 13

# define functions
def initialise(camera="pi"):

	global vs
	
	# if camera != "pi":
	# 	vs = VideoStream(src=camera).start() # initialise using webcam video camera
	# else:	
	# 	vs = VideoStream(usePiCamera=1>0).start() # initialise using picamera

	vs = VideoStream(src=camera).start() # initialise using webcam video camera
	sleep(0.1)
	try:
		vs.read().any()
		return
	except:
		vs = VideoStream(usePiCamera=1>0).start() # initialise using picamera

	sleep(2.0) # give sensor time to warm up

	return

def getFrame():
	frame = vs.read() # read the frame
	frame = imutils.resize(frame, frameDimensions[0]) # resize the frame
	return frame

def blurFrame(frame):

	frame = cv.GaussianBlur(frame,(gaussVal,gaussVal),0) # gaussian blur 
	frame = cv.medianBlur(frame,medBlurVal) # median blur, denoising
	
	return frame

def adjustGamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
	  for i in np.arange(0, 256)]).astype("uint8")

   return cv.LUT(image, table)

def getBallCenter():
    global ballCenter
    global frameDimensions
    
    if ballCenter is not None:
        ballX = int(ballCenter[0]-(frameDimensions[0]/2))
        ballY = int(ballCenter[1]-(frameDimensions[1]/2))
    
        return ballX, ballY

    else:
        return None

initialise(1)

while True:
	raw = getFrame()

	# convert to HSV before blurring to reduce RGB interference in HSV
	hsv = cv.cvtColor(raw, cv.COLOR_BGR2HSV)
	rgb = blurFrame(raw)
	hsv = blurFrame(hsv)

	# splitting to make it easier to use each channel
	hsvHue,hsvSat,hsvVal = cv.split(hsv)
	rgbBlue,rgbGreen,rgbRed = cv.split(rgb)
	
	hsvSatMask = cv.inRange(hsvSat,25,255)

	# removing the blue channel from the red channel leaves the rough location of the ball
	ballGrayscale = cv.subtract(rgbRed,rgbBlue)
	
	# getting the maximum brightness to inRange, using hsvSat as a floor
	maxVal = cv.minMaxLoc(ballGrayscale, hsvSatMask)[1]
	
	# if maxVal < 50, most likely that the ball isn't even in frame
	if maxVal >= 80:

		ballMask = cv.inRange(ballGrayscale, (maxVal-50), 255) # converting to a BW mask
		ballMask = cv.medianBlur(ballMask,17) #	denoise

		# get the center of the mask
		moments = cv.moments(ballMask)

		# weird bug: near the edges of the frame, moments["m00"] = 0, throwing a d0 error
		mDenom = moments["m00"]
		if mDenom == 0:
			mDenom = 1

		ballCenter = int(moments["m10"] / mDenom), int(moments["m01"] / mDenom)
			
	else:
		ballMask = cv.inRange(ballGrayscale, 255, 255) # converting to a BW mask
		ballCenter = None

	print("ballCenter =", ballCenter)
	print("ballCenFxn =", getBallCenter())
	
	if debug: #debug outputs


		ballMaskRGB = cv.cvtColor(ballMask, cv.COLOR_GRAY2BGR)

		cv.circle(ballMaskRGB, ballCenter, 5, (0,0,255), -1) # draw red dot on ball mask at ballCenter
		
		cv.circle(raw, ballCenter, 5, (255,0,0), -1) # draw blue dot on raw at ballCenter

		cv.imshow("No processing", raw)
		#cv.imshow("Processed RGB", rgb)
		cv.imshow("RGB Red", rgbRed)
		#cv.imshow("RGB Green", rgbGreen)
		cv.imshow("RGB Blue", rgbBlue)
		cv.imshow("Ball Gray", ballGrayscale)
		
		#cv.imshow("Processed HSV", hsv)
		#cv.imshow("HSV Hue", hsvHue)
		cv.imshow("HSV Saturation", hsvSatMask)
		#cv.imshow("HSV Value", hsvVal)
		
		cv.imshow("ball mask", ballMaskRGB)

		if cv.waitKey(1) & 0xFF == ord('q'):
			break
			
# do a bit of cleanup
cv.destroyAllWindows()
vs.stop()
