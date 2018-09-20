from imutils.video import VideoStream
import imutils
import numpy as np
import cv2 as cv
from time import sleep

def getCamera(camera=1):
	global rotateFrame
	print("VISION: Getting camera")

	print("VISION: Trying Webcam 1")
	vs = VideoStream(src=1).start() # initialise using webcam video camera
	
	sleep(0.1)
	try:
		vs.read().any()
		rotateFrame = False
		print("VISION: Webcam Success")
	except:
		vs = VideoStream(usePiCamera=1>0).start() # initialise using picamera
		print("VISION: Webcam Failed","VISION: Using PiCamera.",sep='\n')
		sleep(2.0) # give sensor time to warm up

	return vs

vs = getCamera()

def getFrame():
	frame = vs.read()
	frame = imutils.resize(frame, 320)
	return frame

def cleanup():
	print("Doing Cleanup")
	cv.destroyAllWindows()
	vs.stop()

while True:
	#global ballCenter
	rgb = getFrame()

	rgbB,rgbG,rgbR = cv.split(rgb)

	ballGray = cv.subtract(rgbR,cv.addWeighted(rgbB,1,rgbG,1,0))

	cv.imshow("ORIGINAL",rgb)
	cv.imshow("GRAY",ballGray)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cleanup()

# try:
# 	while True:
# 		loop()
# except:
# 	cleanup()