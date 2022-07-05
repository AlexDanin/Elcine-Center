# from Arcanoid import *
# from PyGameClass import *
#
# arc = Arcanoid()
# start = Start()
#
# start.game(arc)

import DataBase as db
import pygame as pg
import sys

pg.init()

sc = pg.display.set_mode((db.WIDTH, db.HEIGHT))
while True:
    for i in range(-100, 100):
        sc.fill((0, 0, 0))
        surf = pg.image.load("img\pointing_up_negate.png")
        sc.blit(surf, (db.WIDTH // 2 - 256 + i, db.HEIGHT // 2 - 256))
        pg.display.update()
    for i in range(100, -100, -1):
        sc.fill((0, 0, 0))
        surf = pg.image.load("img\pointing_up_negate.png")
        sc.blit(surf, (db.WIDTH // 2 - 256 + i, db.HEIGHT // 2 - 256))
        pg.display.update()

# while 1:
#     for i in pg.event.get():
#         if i.type == pg.QUIT:
#             sys.exit()
#
#     pg.time.delay(20)