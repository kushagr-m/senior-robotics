# Strategy

If Ball is in frame 
	If goal is in front *compass*              (45˚ acceptance each side)
	Correct angle to center the ball in frame	
	move forward
		If goal is out of 45˚ acceptance
		Rotate around the ball until goal is in acceptance range
		then forward
	Else
		Move Forward+Right for 1 second
		Turn 90 degrees clockwise
		Move in a counter-clockwise direction 90 degrees around the ball
		Turn 90 degrees clockwise
Else
	Move forward+left for 0.5 seconds
	Rotate counterclockwise 1 revolution
	Move forward+right for 0.5 seconds
	Rotate counterclockwise 1 revolution
	Move backward+right for 0.5 seconds
	Rotate counterclockwise 1 revolution
	Move backward+left for 0.5 seconds
	Rotate counterclockwise 1 revolution

Note:
Revolution and rotation can be approximated through trial and error
