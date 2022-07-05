from Arcanoid import *
from PyGameClass import *
from threading import *
from time import sleep
from HandDetector import *
from Arduino import *
from Timers import *
import DataBase as db


arc = Arcanoid()
start = Start()
hand = Hand()
serial_port = Serial_Arduino()
timer = Timer()

while True:
    if db.step == 0:
        while not db.data_from_arduino:
            serial_port.pull()
        db.step = 1
        # if db.data_from_arduino == "game":
        #     db.step = 1
        # elif db.data_from_arduino == "video":
        #     pass
    elif db.step == 1:
        print("step 1")
        hand.detect_all()
        db.step = 2
    elif db.step == 2:
        start.init()
        db.can_play = True
        thread_start_game = Thread(target=start.game, args=(arc,))
        thread_start_game.start()
        timer.timer_rule(3)
        db.step = 3
    elif db.step == 3:
        t1 = Thread(target=timer.timer_game, args=(5,))
        t1.start()
        hand.detect_one()
