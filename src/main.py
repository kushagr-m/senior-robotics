import vision
import motors

moveBot = True

print("Started MAIN SCRIPT")

while True:
	stop = vision.loop()
	if stop:
		break

	if moveBot: # motors and shit
		centrePadding = 25

		if vision.getBallCenter() is not None:
			ballXPos = getBallCenter()[0]

			if abs(ballXPos) <= centrePadding:
				#do nothing
				pass
			elif ballXPos > 0:
				motors.rotateCenter(direction = 1)
			elif ballXPos < 0:
				motors.rotateCenter(direction = -1)

		else:
			motors.rotateCenter(direction = 1, power = 50)
			
# do a bit of cleanup
vision.cleanup()
print("Script Ended Cleanly")
