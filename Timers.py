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
