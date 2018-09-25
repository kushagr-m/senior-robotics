from vision import VisionProcess
import cv2 as cv

vp = VisionProcess().start(debugLevel=0)

while True:
    try:
        ret, ballCenter, ballCenterQueue = vp.read()
        print(ballCenterQueue)
        if ballCenter is not None: print(ret, ballCenter)

        OutputFrames = vp.OutputFrame()
        outlineCenter, outlineRadius = vp.minEnclosing()

        if OutputFrames[0] is not None:
            CameraOutput = OutputFrames[0]
            
            cv.circle(CameraOutput, ballCenter, 4, (255,0,0), -1)	
            if ballCenter is not None: 
                outlineCenterint = (int(outlineCenter[0]),int(outlineCenter[1]))
                cv.circle(CameraOutput, outlineCenterint, int(outlineRadius), (0,255,0), 3)
                cv.putText(CameraOutput, str(ballCenter),(int(ballCenter[0]+(outlineRadius/90)),int(ballCenter[1]+(outlineRadius/40))),cv.FONT_HERSHEY_DUPLEX,(outlineRadius/100)+0.3,(255,255,255),int((outlineRadius/80)+0.3))		
            cv.imshow('Camera', CameraOutput)
            
        if OutputFrames[1] is not None:	
            cv.imshow('Grayscale Mask', OutputFrames[1])
        if OutputFrames[2] is not None:
            cv.imshow('ballCenter mask', OutputFrames[2])
        if OutputFrames[3] is not None:
            cv.imshow('hsv Mask', OutputFrames[3])
        if cv.waitKey(1) & 0xFF == ord('q'): break

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

vp.stop()