from imutils.video import VideoStream
import imutils
from time import sleep
from threading import Thread
import numpy as np
import cv2 as cv
import collections

class VisionProcess:
	def __init__(self):

		print('Initialising Vision Process...')
		self.frameDimensions = (320,240) # set frame dimensions

		# initialise variables
		self.stopped = False
		self.vs = None
		self.rotateFrame = False
		
		self.noBallDetected = True
		self.currentBallCenter = None
		self.relativeBallCenter = None

		self.outlineCenter, self.outlineRadius = None,None
		self.rgb, self.ballGrayscale, self.ballMask, self.hsvMask = None, None, None, None

		self.ballCenterQueue = collections.deque(maxlen=200)

		print('VisProc: Getting camera.')

		for i in [2,1,0]:
			print('VisProc: Trying webcam ',i,'...',sep='')
			vs = VideoStream(src=i).start()
			sleep(0.1) # warmup time
			try:
				vs.read().any()
				self.vs = vs
				print('VisProc: Webcam',i,'successful.')
				break
			except: pass
		
		if self.vs is None:
			print('VisProc: all webcams unsuccessful.')
			try:
				self.vs = VideoStream(usePiCamera=True).start()
				self.rotateFrame = True
				print('VisProc: PiCamera successful.')
				sleep(2.0)
				vs.read().any()
			except:
				print('VisProc: PiCamera Failed.')
				raise Exception('No camera found.')

	def start(self):
		t = Thread(target=self.Process,args=(),name='VisionProcess')
		t.daemon = True
		t.start()
		return self

	def GetFrame(self):
		rgb = imutils.resize(self.vs.read(),self.frameDimensions[0])
		rgb = cv.GaussianBlur(rgb,(17,17),0)
		if self.rotateFrame:
			rgb = imutils.rotate(rgb,180)
		hsv = cv.cvtColor(rgb, cv.COLOR_BGR2HSV)
		return rgb, hsv

	def OutputFrame(self):
		return self.rgb, self.ballGrayscale, self.ballMask, self.hsvMask

	def Process(self):
		while not self.stopped:

			self.rgb, self.hsv = self.GetFrame()
			rgbB,rgbG,rgbR = cv.split(self.rgb)
			hsvH,hsvS,hsvV = cv.split(self.hsv)
			self.ballGrayscale = cv.subtract(cv.subtract(rgbR,rgbB),rgbG)
			
			self.hsvMask = cv.inRange(hsvS,100,255)
			maxVal = cv.minMaxLoc(self.ballGrayscale, self.hsvMask)[1]

			if maxVal >= 75:

				self.noBallDetected = False

				self.ballMask = cv.bitwise_and(cv.inRange(self.ballGrayscale,(maxVal-45),255),self.hsvMask)

				self.ballMask = cv.dilate(self.ballMask,cv.getStructuringElement(cv.MORPH_ELLIPSE,(17,17)))
				moments = cv.moments(self.ballMask)
				if moments:
					if moments["m00"]<=0: self.currentBallCenter = int(moments["m10"]),int(moments["m01"])
					else: self.currentBallCenter = int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"])
					
					self.ballMask, ballOutline, hierarchy = cv.findContours(self.ballMask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE) # get the outline of self.ballMask
					if ballOutline is not None:
						try:
							self.outlineCenter,self.outlineRadius = cv.minEnclosingCircle(ballOutline[0])
							#if np.linalg.norm(outlineCenter-self.currentBallCenter)>=(outlineRadius*2/3): self.noBallDetected = True
							strX,strY,strW,strH = cv.boundingRect(ballOutline[0])
							outlineRect = cv.minAreaRect(ballOutline[0])
							outlineBox = np.int0(cv.boxPoints(outlineRect))
							if ((outlineRadius/strH)>1) or (strW/strH)>=1.5 or (strH<(outlineRadius*1.5)): 
								self.noBallDetected = True
						except: 
							#print('Could not get outlineCenter and radius')
							pass

				else: self.noBallDetected = True
			else: self.noBallDetected = True

			if self.currentBallCenter is not None:
				self.relativeBallCenter = (int(self.currentBallCenter[0]-(self.frameDimensions[0]/2)), int(self.currentBallCenter[1]-(self.frameDimensions[1]/2)))
				self.ballCenterQueue.append(self.relativeBallCenter)
	
		print('VisProc: Stopped.')
		self.vs.stop()
		return

	def read(self):
		return (not self.noBallDetected), self.relativeBallCenter, self.ballCenterQueue

	def minEnclosing(self):
		if self.outlineCenter and self.outlineRadius: return self.outlineCenter,self.outlineRadius
		else: return None,None

	def stop(self):
		self.stopped = True

