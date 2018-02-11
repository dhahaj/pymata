import sys, signal, pprint
import PyMata.pymata
from Pymata.pymata import *
#followed by another imports your application requires

# create a PyMata instance
# set the COM port string specifically for your platform
board = PyMata("COM5")

# signal handler function called when Control-C occurs
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!!!!')
    if board != None:
        board.reset()
    sys.exit(0)
    # listen for SIGINT
    signal.signal(signal.SIGINT, signal_handler)
