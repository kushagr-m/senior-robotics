from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import cv2
import picamera

debug = True

frameDimensions = 320,240
medianKey = 15

def emptyCallback(value):
	pass

vs = WebcamVideoStream(src=0).start()

def getFrame():

	frame = vs.read()
	frame = imutils.resize(frame, frameDimensions[0])

	return frame

def processFrame(frame):
	
	frame = cv2.medianBlur(frame,medianKey)
	
	return frame

while True:
	
	raw = getFrame()
	
	hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)

	rgb = processFrame(raw)
	hsv = processFrame(hsv)

	hsvHue,hsvSat,hsvVal = cv2.split(hsv)
	rgbBlue,rgbGreen,rgbRed = cv2.split(rgb)

	if debug:

		cv2.imshow("No processing", raw)
		cv2.imshow("Processed RGB", rgb)
		cv2.imshow("Processed HSV", hsv)

		cv2.imshow("RGB Red", rgbRed)
		cv2.imshow("RGB Green", rgbGreen)
		cv2.imshow("RGB Blue", rgbBlue)

		cv2.imshow("HSV Hue", hsvHue)
		cv2.imshow("HSV Saturation", hsvSat)
		cv2.imshow("HSV Value", hsvVal)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
