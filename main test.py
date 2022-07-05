from Arcanoid import *
from PyGameClass import *
from threading import *
from time import sleep
from HandDetector import *
from Arduino import *
from Timers import *


arc = Arcanoid()
start = Start()
hand = Hand()
serial_port = Serial_Arduino()
timer = Timer()

while not db.data_from_arduino:
    serial_port.pull()

print(1)

hand.detect_all()

start.init()

print(2)

t2 = Thread(target=start.game, args=(arc,))
t2.start()

timer.timer_rule(3)

t1 = Thread(target=timer.timer_game, args=(5,))
t1.start()

hand.detect_one()

t1.join()
t2.join()



# from HandDetector import *
#
# hand = Hand()
# hand.detect_all()
# hand.detect_one()