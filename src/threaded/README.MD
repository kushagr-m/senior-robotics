# VisionProcess
Runs ball detection vision code in its own thread.  
Based on the threading implementation of `imutils`.


# Usage:
```python
from path.to.vision import VisionProcess
vp = VisionProcess().start()

While True: # in the loop
	try: 
		ret, current, queue = vp.read()
		circleCenter, circleRadius = vp.minEnclosing()
		# ...
		# write all code here.
		# ...
	
	except KeyboardInterrupt:
		break

vp.stop()

```
---


## Values:

### `ret`
Is the ball detected?  
Outputs = `True`/`False`  

### `current`
The **current ball position, relative to the center of the frame**   
Outputs = `(x,y)` (is a tuple)  
*x* = `[-160,160]`  
*y* = `[-120,120]`

### `queue`
History of all ball positions  
Outputs a queue.

---

### **NOTE:** The following two values should not be considered reliable.

### `circleCenter`
The **centre of a circle surrounding the ball**   
Outputs = `(x,y)` (is a tuple) 

### `circleRadius`
The **radius of a circle surrounding the ball**  
Outputs a **float**.

---
