# VisionProcess
## How to use
To initialise:
```python
from vision import VisionProcess
vp = VisionProcess().start(debugLevel=0)
```

## Usages:
```python
While True:
	try: 
		ret, current, queue = vp.read()
	exce

```

### `ret`
Is the ball detected?  
Outputs = `True`/`False`  


### `current`
The **current ball position**   
Outputs = `(x,y)` (is a tuple)  

### `queue`
History of all ball positions  
Outputs a queue.