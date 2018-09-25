from imutils.video import VideoStream
import imutils
import numpy as numpy
import cv2 as cv
import time
import math as maths
import collections
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="output.avi", help="/path/to/output.avi")
ap.add_argument("-f", "--fps", default=32,help="output FPS")

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

while True:
	cv.imshow("camera",vs.read())
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cv.destroyAllWindows()
vs.stop()