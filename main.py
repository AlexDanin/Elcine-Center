from Arcanoid import Arcanoid
import pygame as pg
import DataBase as db

pg.init()
db.screen = pg.display.set_mode((db.WIDTH, db.HEIGHT))
clock = pg.time.Clock()

arc = Arcanoid()

while True:
    db.screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    arc.run()

    pg.display.flip()
    clock.tick(db.fps)