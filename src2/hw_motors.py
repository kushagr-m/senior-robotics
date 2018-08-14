import serial
from time import sleep
ser = serial.Serial('/dev/ttyACM0',115200) # change to ACM1 if that is the USB port
#AMA0
FLPower = 0
FRPower = 0
BRPower = 0
BLPower = 0

motorDebug = True

	

# motor control functions
# converts python to arduino

def FL(power = 100):
	global FLPower
	if power is not FLPower:
		FLPower = power
		if (power >= 0):
			out = "a"
		elif (power < 0):
			out = "A"
		out = str(abs(power)) + out + "\n"
		if motorDebug:
			print(out)
		ser.write(str.encode(out))
	return

def FR(power = 100):
	global FRPower
	if power is not FRPower:
		FRPower = power
		if (power >= 0):
			out = "b"
		elif (power < 0):
			out = "B"
		out = str(abs(power)) + out + "\n"
		if motorDebug:
			print(out)
		ser.write(str.encode(out))
	return

def BR(power = 100):
	global BRPower
	if power is not BRPower:
		BRPower = power
		if (power >= 0):
			out = "d"
		elif (power < 0):
			out = "D"
		out = str(abs(power)) + out + "\n"
		if motorDebug:
			print(out)
		ser.write(str.encode(out))
	return

def BL(power = 100):
	global BLPower
	if power is not BLPower:
		BLPower = power
		if (power >= 0):
			out = "c"
		elif (power < 0):
			out = "C"
		out = str(abs(power)) + out + "\n"
		if motorDebug:
			print(out)
		ser.write(str.encode(out))
	return

# motor helper functions
def stop():
	FL(0)
	FR(0)
	BR(0)
	BL(0)
	return

# GO IN A CERTAIN DIRECTION
# power = between [-100,100]
def goStraight(power = 100):
	FR(power)
	FL(-1*power)
	BR(power)
	BL(-1*power)
	return

def goLeft(power = 100):
	FR(power)
	FL(power)
	BR(-1*power)
	BL(-1*power)
	return

def goRight(power = 100):
	FR(-1*power)
	FL(-1*power)
	BR(power)
	BL(power)
	return

def goBack(power = 100):
	FR(-1*power)
	FL(power)
	BR(-1*power)
	BL(power)
	return

def goFR(power = 100):
	FL(-1*power)
	FR(0)
	BL(0)
	BR(power)
	return

def goFL(power = 100):
	FL(0)
	FR(power)
	BL(-1*power)
	BR(0)
	return

def goBR(power = 100):
	FL(0)
	FR(-1*power)
	BL(power)
	BR(0)
	return

def goBL(power = 100):
	FL(power)
	FR(0)
	BL(0)
	BR(-1*power)
	return

def rotateCenter(direction = -1, power = 100):

	# negative is counterclockwise, positive is clockwise

	if direction < 0:
		#counterclockwise
		#FR(100)
		#FL(100)
		#BR(100)
		#BL(100)
		#sleep(0.1)
		FR(power)
		FL(power)
		BR(power)
		BL(power)

	if direction > 0:
		#clockwise
		#FR(-100)
		#FL(-100)
		#BR(-100)
		#BL(-100)
		#sleep(0.1)
		FR(-1*power)
		FL(-1*power)
		BR(-1*power)
		BL(-1*power)

	return

def rotateFrAxis(direction = -1, power = 100):

	if direction < 0:
		#counterclockwise
		FR(0)
		FL(0)
		BR(-1*power)
		BL(-1*power)

	if direction > 0:
		#clockwise
		FR(0)
		FL(0)
		BR(power)
		BL(power)

	return