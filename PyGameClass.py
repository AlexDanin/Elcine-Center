import pygame
from DataBase import *


class Start:
    def __init__(self):
        pygame.init()
        self.sc = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.flag = True

    def game(self, copy):
        while self.flag:
            self.sc.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            copy.run()
            copy.control()

            pygame.display.flip()
            self.clock.tick(self.fps)
