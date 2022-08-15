from time import sleep as sl
import DataBase as db
import pygame


class Timer:
    def __init__(self):
        pass

    def timer_game(self, number):
        for i in range(number, 0, -1):
            db.seconds = i
            sl(1)
        db.game = True

    def timer_rule(self, number):
        for i in range(number, 0, -1):
            sl(1)
        db.rule = False

    def timer_off(self):
        i = 10
        while i > 0:
            if db.off:
                i -= 1
                sl(1)
                print(i)
            else:
                print("break")
                break

        if i <= 0:
            db.push = True

    def timer_wait(self):
        i = 0
        while db.wait:
            db.img = db.gif[i % len(db.gif)]
            i += 1
            sl(0.2)

    def timer_gif(self):
        i = 0
        while db.wait:
            db.img = db.gif[i % len(db.gif)]
            i += 1
            sl(0.2)


