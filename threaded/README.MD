# VisionProcess
Runs ball detection vision code in its own thread.  
Based on the threading implementation of `imutils`.


# Usage:
```python
from vision import VisionProcess
vp = VisionProcess().start(debugLevel=0)

While True: # in the loop
	try: 
		ret, current, queue = vp.read()
		circleCenter, circleRadius = vp.minEnclosing()
		# ...
		# write all code here.
		# ...
	except KeyboardInterrupt: # Ctrl+C
		break

vp.stop()

```
---


## Values:

### `ret`
Is the ball detected?  
Outputs = `True`/`False`  

### `current`
The **current ball position**   
Outputs = `(x,y)` (is a tuple)  

### `queue`
History of all ball positions  
Outputs a queue.

---

### **NOTE:** The following two values should not be considered reliable.

### `circleCenter`
The **centre of the circle surrounding the ball**   
Outputs = `(x,y)` (is a tuple) 

### `circleRadius`
The **radius of the circle surrounding the ball**  
Outputs a **float**.

---
