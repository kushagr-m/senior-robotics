from imutils.video import WebcamVideoStream
import imutils
import cv2

debug = True

resizeDimensions = 320,240

vs = WebcamVideoStream(src=1).start()
time.sleep(0.1)

def processFrame(frame):
	frame = imutils.resize(frame, resizeDimensions[0])
	frame = cv2.GaussianBlur(frame,(9,9),0)
	frame = cv2.medianBlur(frame,9)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	return frame, hsv

# loop over some frames...this time using the threaded stream
while True:
	frame, hsv = processFrame(vs.read())

	if debug:
		cv2.imshow("hsv", hsv)
		cv2.imshow("rgb", frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()