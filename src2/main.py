import hw_motors as motors
from hw_read import *

from ai_attack import *
from ai_defend import *

botMode = 0
# 0 = attack
# 1 = defend

while True:

	if botMode == 0:
		attack()

	elif botMode == 1:
		defend()