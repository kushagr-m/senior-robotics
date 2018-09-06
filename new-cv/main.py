from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import cv2 as cv

debug = True

frameDimensions = 320,240
medBlurVal = 13
gaussVal = 13

gammaVal = 0.3

webcamSource = 1

dilateKernel = 19,19

def getFrame():

	frame = vs.read() # read the frame
	frame = imutils.resize(frame, frameDimensions[0]) # resize the frame

	return frame

def blurFrame(frame):

	#frame = cv.GaussianBlur(frame,(gaussVal,gaussVal),0) # gaussian blur 
	frame = cv.medianBlur(frame,medBlurVal) # median blur
	frame = adjustGamma(frame, gammaVal) # log darken to make extreme colours brighter
	
	return frame

def adjustGamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv.LUT(image, table)

def empty(input):
	pass

vs = WebcamVideoStream(src=webcamSource).start()
while True:
	
	raw = getFrame()

	hsv = cv.cvtColor(raw, cv.COLOR_BGR2HSV)

	rgb = blurFrame(raw)
	hsv = blurFrame(hsv)

	hsvHue,hsvSat,hsvVal = cv.split(hsv)
	rgbBlue,rgbGreen,rgbRed = cv.split(rgb)

	ballMaskGray = adjustGamma(cv.subtract(rgbRed,rgbBlue), 0.7)
	
	ballMaskBW = cv.inRange(ballMaskGray,150,255)

	ballMaskBW = cv.dilate(ballMaskBW,dilateKernel)

	if debug:

		cv.imshow("No processing", raw)
		cv.imshow("Processed RGB", rgb)
		cv.imshow("Processed HSV", hsv)

		cv.imshow("RGB Red", rgbRed)
		cv.imshow("RGB Green", rgbGreen)
		cv.imshow("RGB Blue", rgbBlue)


		cv.imshow("HSV Hue", hsvHue)
		cv.imshow("HSV Saturation", hsvSat)
		cv.imshow("HSV Value", hsvVal)
		
		cv.imshow("red-blue", ballMaskGray)

		cv.imshow("ball mask", ballMaskBW)
		#cv.imshow("ball inrange", ballMaskBW)

		if cv.waitKey(1) & 0xFF == ord('q'):
			break


# do a bit of cleanup
cv.destroyAllWindows()
vs.stop()
