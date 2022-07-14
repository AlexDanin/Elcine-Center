import time

import pygame

import DataBase as db
from HandDetector import Hand
from Arduino import Serial_Arduino
from Timers import Timer
import numpy as np
import cv2
from threading import Thread


class Start:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.flag = True
        pygame.font.init()
        self.font_timer_game = pygame.font.Font(None, 200)
        self.font_timer_home = pygame.font.Font(None, 700)
        self.font_lose = pygame.font.Font(None, 150)
        self.font_win = pygame.font.Font(None, 150)

        # window
        self.h = db.HEIGHT * db.k_screen
        self.w = self.h * 1.5
        self.left = (db.WIDTH - self.w) // 2
        self.top = (db.HEIGHT - self.h) // 2

        # classes
        self.hand = Hand()
        self.serial_port = Serial_Arduino()
        self.timer = Timer()

    def init(self):
        pygame.init()
        db.screen = pygame.display.set_mode((db.WIDTH, db.HEIGHT))

    def quit(self):
        pygame.display.quit()
        cv2.destroyAllWindows()

    def draw_timer_game(self):
        if not db.game:
            text = self.font_timer_game.render(str(db.seconds), True, (255, 255, 255))
            db.screen.blit(text, (db.WIDTH // 2 - 50, db.HEIGHT // 2 - 100))

    def draw_timer_home(self):
        text = self.font_timer_home.render(str(db.seconds), True, (15, 15, 255))
        scale = pygame.transform.scale(
            text, (self.w // 2, self.h))

        scale_rect = scale.get_rect(
            center=(db.WIDTH // 2 + scale.get_width() // 2, db.HEIGHT // 2))

        db.screen.blit(scale, scale_rect)
        # db.screen.blit(text, (db.WIDTH - self.left * 4, db.HEIGHT / 2 - self.top * 2.8))

    def draw_rules(self):
        surf = pygame.image.load("img\pointing_up_negate.png")
        scale = pygame.transform.scale(
            surf, (self.w // 2, self.w // 2))

        scale_rect = scale.get_rect(
            center=(db.WIDTH // 2 + scale.get_width() // 2, db.HEIGHT // 2))

        db.screen.blit(scale, scale_rect)
        # for i in range(-150, 150):
        #     db.screen.fill((0, 0, 0))
        #     db.screen.blit(surf, (db.WIDTH // 2 - 256 + i, db.HEIGHT // 2 - 256))
        #     pygame.display.flip()
        # for i in range(150, -150, -1):
        #     db.screen.fill((0, 0, 0))
        #     db.screen.blit(surf, (db.WIDTH // 2 - 256 + i, db.HEIGHT // 2 - 256))
        #     pygame.display.flip()

    def draw_game_over(self):
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        text = self.font_lose.render("Game Over", True, (255, 100, 100))
        scale_rect = text.get_rect(
            center=(db.WIDTH // 2, db.HEIGHT // 2))
        db.screen.blit(text, scale_rect)

    def draw_win(self):
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        text = self.font_win.render("Win", True, (100, 255, 100))
        scale_rect = text.get_rect(
            center=(db.WIDTH // 2, db.HEIGHT // 2))
        db.screen.blit(text, scale_rect)

    def draw_off(self):
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        text = self.font_win.render("OFF", True, (255, 0, 0))
        scale_rect = text.get_rect(
            center=(db.WIDTH // 2, db.HEIGHT // 2))
        db.screen.blit(text, scale_rect)

    def draw_home_screen(self):
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        pygame.draw.line(db.screen, (255, 255, 255), (db.WIDTH // 2, self.top - 20),
                         (db.WIDTH // 2, db.HEIGHT - self.top + 19), 1)
        # Изображение с камеры
        frame = cv2.cvtColor(self.hand.get_img(), cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = cv2.flip(frame, 0)
        frame = cv2.resize(frame, (345, 460))
        frame = pygame.surfarray.make_surface(frame)
        db.screen.blit(frame, (int(self.left), int(self.top)))
        # pygame.draw.rect(db.screen, (100, 165, 15),
        #                  (int(self.left), int(self.top), int(self.w // 2 - 20), int(self.h - 10)))

    def play(self, copy):
        while db.can_play:
            if db.hand_here:
                db.screen.fill((0, 0, 0))
                copy.run()
                copy.control(db.hand['lmList'][8][:2][0])
                # print(self.clock.get_fps())
                pygame.display.flip()
                self.clock.tick(30)

    def game(self, copy):

        while self.flag:
            if db.step == "wait":
                if db.data_from_arduino == "video":
                    self.serial_port.pull()
                    if db.data_from_arduino == "game":
                        db.step = "init"
            elif db.step == "init":
                self.init()
                db.was_init = True
                db.step = "timer_off"
            elif db.step == "timer_off":
                db.off = True
                t0 = Thread(target=self.timer.timer_off)
                t0.start()
                db.step = "detect_all"

            elif db.step == "detect_all":
                self.hand.detect_all()
                if db.hand_start:
                    db.step = "start_game_timer"
                    db.hand_start = False

                db.screen.fill((0, 0, 0))
                self.draw_home_screen()
                self.draw_rules()
                pygame.display.flip()

                if not db.hand_here and not db.off:
                    db.step = "timer_off"
                    db.off = True
                elif db.hand_here:
                    print("here")
                    db.off = False

            elif db.step == "start_game_timer":
                t1 = Thread(target=self.timer.timer_game, args=(5,))
                t1.start()
                db.step = "detect_one"

            elif db.step == "detect_one":
                self.hand.detect_one()
                db.screen.fill((0, 0, 0))
                self.draw_home_screen()
                self.draw_timer_home()
                pygame.display.flip()

                if db.game:
                    db.step = "game"
                    db.game = False
                    db.can_play = True
                    copy.__init__()
                    t3 = Thread(target=self.play, args=(copy,))
                    t3.start()

            elif db.step == "timer_one_off":
                db.off = True
                t4 = Thread(target=self.timer.timer_off)
                t4.start()
                db.step = "game"

            elif db.step == "game":
                self.hand.detect_one()

                if db.win_or_lose == 1:
                    db.step = "win"
                    db.can_play = False
                    # db.can_hand_one = False
                elif db.win_or_lose == 2:
                    db.step = "lose"
                    db.can_play = False
                    # db.can_hand_one = False

                if not db.hand_here and not db.off:
                    db.step = "timer_one_off"
                    db.off = True
                elif db.hand_here:
                    print("here")
                    db.off = False

            elif db.step == "win":
                db.screen.fill((0, 0, 0))
                self.draw_win()
                pygame.display.flip()
                time.sleep(3)
                db.step = "detect_all"
                db.win_or_lose = 0

            elif db.step == "lose":
                db.screen.fill((0, 0, 0))
                self.draw_game_over()
                pygame.display.flip()
                time.sleep(3)
                db.step = "detect_all"
                db.win_or_lose = 0

            if db.was_init:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

                pygame.display.flip()

            if db.push:
                print("off")
                db.screen.fill((0, 0, 0))
                self.draw_off()
                pygame.display.flip()
                time.sleep(2)
                self.serial_port.push()
                self.quit()
                db.step = "wait"
                db.data_from_arduino = "video"
                db.push = False
                db.was_init = False

            self.clock.tick(db.fps)
