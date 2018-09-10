def FL(power = 100):
	print("a"+power)
	return

def FR(power = 100):
	print("b"+power)
	return

def BR(power = 100):
	print("c"+power)
	return

def BL(power = 100):
	print("d"+power)
	return


# Reset (stop all movement)
def stop():
	FL(0)
	FR(0)
	BL(0)
	BR(0)
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

def rotateCenter(direction = "left", power = 100):

	if direction == "left":
		#counterclockwise
		FR(power)
		FL(power)
		BR(power)
		BL(power)

	if direction == "right":
		#clockwise
		FR(-1*power)
		FL(-1*power)
		BR(-1*power)
		BL(-1*power)

	return

def rotateFrAxis(direction = "left", power = 100):

	if direction == "left":
		#counterclockwise
		FR(0)
		FL(0)
		BR(-1*power)
		BL(-1*power)

	if direction == "right":
		#clockwise
		FR(0)
		FL(0)
		BR(power)
		BL(power)

	return