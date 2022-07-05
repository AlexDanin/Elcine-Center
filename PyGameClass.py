import pygame

import DataBase as db


class Start:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.flag = True
        pygame.font.init()
        self.font = pygame.font.Font(None, 200)

    def init(self):
        pygame.init()
        db.screen = pygame.display.set_mode((db.WIDTH, db.HEIGHT))

    def quit(self):
        pygame.quit()

    def draw_timer(self):
        if not db.game:
            text = self.font.render(str(db.seconds), True, (255, 255, 255))
            db.screen.blit(text, (db.WIDTH // 2 - 50, db.HEIGHT // 2 - 100))

    def rules(self):
        surf = pygame.image.load("img\pointing_up_negate.png")
        for i in range(-150, 150):
            db.screen.fill((0, 0, 0))
            db.screen.blit(surf, (db.WIDTH // 2 - 256 + i, db.HEIGHT // 2 - 256))
            pygame.display.flip()
        for i in range(150, -150, -1):
            db.screen.fill((0, 0, 0))
            db.screen.blit(surf, (db.WIDTH // 2 - 256 + i, db.HEIGHT // 2 - 256))
            pygame.display.flip()

    def game(self, copy):
        while self.flag:
            db.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            if db.rule:
                self.rules()
            else:
                if db.game:
                    try:
                        copy.run()
                        copy.control(db.hand['lmList'][8][:2][0])
                    except Exception:
                        print("None hand")
                else:
                    try:
                        copy.delay()
                        copy.control(db.hand['lmList'][8][:2][0])
                    except Exception:
                        pass
                    self.draw_timer()

                pygame.display.flip()
                self.clock.tick(db.fps)
