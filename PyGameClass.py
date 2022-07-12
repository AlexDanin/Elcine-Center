import pygame

import DataBase as db


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

    def init(self):
        pygame.init()
        db.screen = pygame.display.set_mode((db.WIDTH, db.HEIGHT))

    def quit(self):
        pygame.quit()

    def draw_timer_game(self):
        if not db.game:
            text = self.font_timer_game.render(str(db.seconds), True, (255, 255, 255))
            db.screen.blit(text, (db.WIDTH // 2 - 50, db.HEIGHT // 2 - 100))

    def draw_timer_home(self):
        text = self.font_timer_home.render("3", True, (15, 15, 255))
        db.screen.blit(text, (db.WIDTH - self.left * 4, db.HEIGHT / 2 - self.top * 2.8))

    def draw_rules(self):
        surf = pygame.image.load("img\pointing_up_negate.png")
        for i in range(-150, 150):
            db.screen.fill((0, 0, 0))
            db.screen.blit(surf, (db.WIDTH // 2 - 256 + i, db.HEIGHT // 2 - 256))
            pygame.display.flip()
        for i in range(150, -150, -1):
            db.screen.fill((0, 0, 0))
            db.screen.blit(surf, (db.WIDTH // 2 - 256 + i, db.HEIGHT // 2 - 256))
            pygame.display.flip()

    def draw_game_over(self):
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        text = self.font_lose.render("Game Over", True, (255, 100, 100))
        db.screen.blit(text, (self.left + 75, db.HEIGHT // 2 - 75))

    def draw_win(self):
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        text = self.font_win.render("Win", True, (100, 255, 100))
        db.screen.blit(text, (self.left * 2 + 20, db.HEIGHT // 2 - 75))

    def draw_home_screen(self):
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        pygame.draw.line(db.screen, (255, 255, 255), (db.WIDTH // 2, self.top - 20),
                         (db.WIDTH // 2, db.HEIGHT - self.top + 19), 1)
        # Изображение с камеры
        pygame.draw.rect(db.screen, (100, 165, 15),
                         (int(self.left), int(self.top), int(self.w // 2 - 20), int(self.h - 10)))


    def game(self, copy):
        while self.flag:
            db.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # if db.rule:
            #     self.rules()
            # else:
            #     if db.game:
            #         try:
            #             copy.run()
            #             copy.control(db.hand['lmList'][8][:2][0])
            #         except Exception:
            #             print("None hand")
            #     else:
            #         try:
            #             copy.delay()
            #             copy.control(db.hand['lmList'][8][:2][0])
            #         except Exception:
            #             pass
            #         self.draw_timer()
            # copy.delay()
            # copy.control()
            self.draw_home_screen()
            self.draw_timer_home()

            pygame.display.flip()
            self.clock.tick(db.fps)
