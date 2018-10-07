from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from time import sleep

board = PyMata3()
board.set_pin_mode(0, Constants.ANALOG)

while True:
    print(board.analog_read(0))
    sleep(1)