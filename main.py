from test import *
from PyGameClass import *
import pygame as pg
from threading import *
from time import sleep

pg.init()

screen = pg.display.set_mode((500, 700))
clock = pg.time.Clock()

arc = Arcanoid()
st = Start()


def timer(number):
    for i in range(number, 0, -1):
        print(i)
        sleep(1)
    st.flag = False


t2 = Thread(target=timer, args=(8,))
t1 = Thread(target=st.game, args=(arc,))

t1.start()
t2.start()

t1.join()
t2.join()