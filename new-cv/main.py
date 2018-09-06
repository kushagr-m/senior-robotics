from imutils.video import VideoStream
import imutils
import numpy as np
import cv2 as cv
from time import sleep

debug = True

frameDimensions = 320,240
medBlurVal = 13
gaussVal = 13

dilateKernel = 19,19

# define functions
def initialise(camera="pi"):

	global vs
	
	if camera != "pi":
		vs = VideoStream(src=camera).start() # initialise using webcam video camera
	else:	
		vs = VideoStream(usePiCamera=1>0).start() # initialise using picamera

	sleep(2.0) # give sensor time to warm up

	return

def getFrame():
	frame = vs.read() # read the frame
	frame = imutils.resize(frame, frameDimensions[0]) # resize the frame
	return frame

def blurFrame(frame):

	frame = cv.GaussianBlur(frame,(gaussVal,gaussVal),0) # gaussian blur 
	frame = cv.medianBlur(frame,medBlurVal) # median blur
	
	return frame

def adjustGamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
	  for i in np.arange(0, 256)]).astype("uint8")

   return cv.LUT(image, table)

initialise()

while True:
	raw = getFrame()

	hsv = cv.cvtColor(raw, cv.COLOR_BGR2HSV)

	rgb = blurFrame(raw)
	hsv = blurFrame(hsv)

	hsvHue,hsvSat,hsvVal = cv.split(hsv)
	rgbBlue,rgbGreen,rgbRed = cv.split(rgb)

	ballGrayscale = cv.subtract(rgbRed,rgbBlue)
	
	(minVal,maxVal,minLoc,maxLoc) = cv.minMaxLoc(ballGrayscale, cv.inRange(hsvSat,25,255))
	
	if maxVal >= 80:
		ballMask = cv.inRange(ballGrayscale, (maxVal-50), 255)
		ballMask = cv.medianBlur(ballMask,17)
		moments = cv.moments(ballMask)
		ballCenter = int(moments["m10"] / moments["m00"]),int(moments["m01"] / moments["m00"])
			
	else:
		ballMask = cv.inRange(ballGrayscale, 255, 255)
		ballCenter = None
			
	print(ballCenter)

	if debug:

		ballMaskRGB = cv.cvtColor(ballMask, cv.COLOR_GRAY2BGR)

		cv.circle(ballMaskRGB, ballCenter, 5, (0,0,255), -1) # red ballCenter from moments
		
		cv.circle(raw, ballCenter, 5, (255,0,0), -1) # blue from moments

		cv.imshow("No processing", raw)
		#cv.imshow("Processed RGB", rgb)
		#cv.imshow("RGB Red", rgbRed)
		#cv.imshow("RGB Green", rgbGreen)
		#cv.imshow("RGB Blue", rgbBlue)
		
		#cv.imshow("Processed HSV", hsv)
		#cv.imshow("HSV Hue", hsvHue)
		#cv.imshow("HSV Saturation", hsvSat)
		#cv.imshow("HSV Value", hsvVal)
		
		cv.imshow("ball mask", ballMaskRGB)

		if cv.waitKey(1) & 0xFF == ord('q'):
			break


# do a bit of cleanup
cv.destroyAllWindows()
vs.stop()
