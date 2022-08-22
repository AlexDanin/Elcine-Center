import sys
import time

import pygame
from random import randrange as rnd
from DataBase import *
import DataBase as db
import keyboard


class Arcanoid:
    def __init__(self):
        pygame.mixer.init()
        self.pong_sound = pygame.mixer.Sound("music/Pong.wav")
        self.crush_sound = pygame.mixer.Sound('music/Crush.wav')
        self.fall_sound = pygame.mixer.Sound('music/Fall.wav')
        self.wall_sound = pygame.mixer.Sound('music/Wall.wav')
        self.menu_sound = pygame.mixer.Sound('music/menu.mp3')

        print(db.cam_h, db.cam_w)
        self.quotient_h = db.HEIGHT // db.cam_h + 1
        self.quotient_w = db.WIDTH // db.cam_w + 1

        self.h = db.HEIGHT * db.k_screen
        self.w = self.h * 1.5

        self.left = (db.WIDTH - self.w) // 2
        self.top = (db.HEIGHT - self.h) // 2
        print(self.w, self.h, self.left, self.top)

        self.minimum_distance = 25
        self.maximum_distance = 100

        # blocks settings
        self.block_w = self.w // 10
        self.block_h = self.h // 10
        print(self.block_h, self.block_w)
        self.block_list = [
            pygame.Rect(self.left + self.block_w * i, self.top + self.block_h * j, self.block_w - 10, self.block_h - 10)
            for i in range(10) for j in range(4)]
        self.color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

        # paddle settings
        self.paddle_w = self.block_w * 2 + 10
        self.paddle_h = self.block_h // 2
        self.paddle_speed = self.w // 80
        self.paddle = pygame.Rect(WIDTH // 2 - self.paddle_w // 2, HEIGHT - self.top - self.paddle_h - 10,
                                  self.paddle_w,
                                  self.paddle_h)
        self.paddle_collision = pygame.Rect(WIDTH // 2 - self.paddle_w // 2 - 20,
                                            HEIGHT - self.top - self.paddle_h - 10 - 20,
                                            self.paddle_w + 20,
                                            self.paddle_h)

        # ball settings
        self.ball_radius = self.block_h * 0.3
        self.ball_speed = self.w // 200
        self.ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.ball = pygame.Rect(rnd(self.ball_rect + self.left, WIDTH - self.ball_rect - self.left), HEIGHT // 2,
                                self.ball_rect,
                                self.ball_rect)
        self.dx, self.dy = 1, -1

        pygame.font.init()
        self.font_timer_game = pygame.font.Font(None, 250)
        self.font_lose = pygame.font.Font(None, 350)
        self.font_win = pygame.font.Font(None, 350)
        self.clock = pygame.time.Clock()

    def gif(self):
        db.screen.fill((0, 0, 0))

        dog_surf = pygame.image.load(db.img)
        scale = pygame.transform.scale(
            dog_surf, (dog_surf.get_width() * 5,
                       dog_surf.get_height() * 5))
        scale_rect = scale.get_rect(
            center=(db.WIDTH // 2, db.HEIGHT // 2))
        # print(db.img)
        db.screen.blit(scale, scale_rect)
        pygame.display.flip()

    def init(self):
        pygame.init()
        db.screen = pygame.display.set_mode((db.WIDTH, db.HEIGHT))

    def quit(self):
        pygame.display.quit()

    def draw(self):
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        [pygame.draw.rect(db.screen, self.color_list[color], block) for color, block in enumerate(self.block_list)]
        pygame.draw.rect(db.screen, pygame.Color('darkorange'), self.paddle)
        pygame.draw.circle(db.screen, pygame.Color('white'), self.ball.center, self.ball_radius)
        try:
            pygame.draw.circle(db.screen, pygame.Color('yellow'),
                               (db.hand[0] * self.quotient_w, db.hand[1] * self.quotient_h), self.block_h * 0.1)
        except Exception:
            pass

    def detect_collision(self, dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    def ball_movement(self):
        self.ball.x += self.ball_speed * self.dx
        self.ball.y += self.ball_speed * self.dy

    def ball_collision(self):
        # collision left right
        if self.ball.centerx < self.ball_radius + self.left or self.ball.centerx > WIDTH - self.ball_radius - self.left:
            self.dx = -self.dx
            self.wall_sound.play()
        # collision top
        if self.ball.centery < self.ball_radius + self.top:
            self.dy = -self.dy
            self.wall_sound.play()
        # collision paddle
        if self.ball.colliderect(self.paddle) and self.dy > 0:
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, self.ball, self.paddle)
            self.pong_sound.play()
        # collision blocks
        hit_index = self.ball.collidelist(self.block_list)
        if hit_index != -1:
            self.crush_sound.play()
            hit_rect = self.block_list.pop(hit_index)
            hit_color = self.color_list.pop(hit_index)
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, self.ball, hit_rect)
            # special effect
            hit_rect.inflate_ip(self.ball.width * 3, self.ball.height * 3)
            pygame.draw.rect(db.screen, hit_color, hit_rect)

    def follow_me(self, pops, fpos):
        target_vector = pygame.math.Vector2(*pops)
        follower_vector = pygame.math.Vector2(*fpos)
        new_follower_vector = pygame.math.Vector2(*fpos)

        distance = follower_vector.distance_to(target_vector)
        if distance > self.minimum_distance:
            direction_vector = (target_vector - follower_vector) / distance
            min_step = max(0, int(distance - self.maximum_distance))
            max_step = distance - self.minimum_distance
            step_distance = min_step + (max_step - min_step) * 0.1
            new_follower_vector = follower_vector + direction_vector * step_distance

        return new_follower_vector.x

    def control(self, hand_pos):
        if hand_pos[0] - (self.paddle_w // 2) > self.left and hand_pos[0] + (
                self.paddle_w // 2) < WIDTH - self.left - 12:
            self.paddle.centerx = self.follow_me(hand_pos, (self.paddle.centerx, self.paddle.centery))
            self.paddle_collision.centerx = hand_pos[0]

        # if hand_pos_x - (self.paddle_w // 2) > self.left and hand_pos_x + (self.paddle_w // 2) < WIDTH - self.left - 12:
        #     self.paddle.centerx = hand_pos_x
        #     self.paddle_collision.centerx = hand_pos_x
        # else:
        #     if hand_pos_x > WIDTH / 2:
        #         self.paddle.centerx = self.left - (self.paddle_w // 2)
        #         self.paddle_collision.centerx = self.left - (self.paddle_w // 2)
        #     else:
        #         self.paddle.centerx = self.left + (self.paddle_w // 2)
        #         self.paddle_collision.centerx = self.left + (self.paddle_w // 2)

        # if keyboard.is_pressed('Left') and self.paddle.left > self.left:
        #     self.paddle.left -= self.paddle_speed
        # if keyboard.is_pressed('Right') and self.paddle.right < WIDTH - self.left - 12:
        #     self.paddle.right += self.paddle_speed

    def win_game_over(self):
        if self.ball.bottom > HEIGHT - self.top:
            self.fall_sound.play()
            db.win_or_lose = 2
        elif not len(self.block_list):
            self.fall_sound.play()
            db.win_or_lose = 1

    def draw_game_over(self):
        db.screen.fill((0, 0, 0))
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        text = self.font_lose.render("Game Over", True, (255, 100, 100))
        scale_rect = text.get_rect(
            center=(db.WIDTH // 2, db.HEIGHT // 2))
        db.screen.blit(text, scale_rect)
        pygame.display.flip()
        time.sleep(3)

    def draw_win(self):
        db.screen.fill((0, 0, 0))
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        text = self.font_win.render("Win", True, (100, 255, 100))
        scale_rect = text.get_rect(
            center=(db.WIDTH // 2, db.HEIGHT // 2))
        db.screen.blit(text, scale_rect)
        pygame.display.flip()
        time.sleep(3)

    def draw_off(self):
        db.screen.fill((0, 0, 0))
        pygame.draw.rect(db.screen, (255, 255, 255),
                         (int(self.left - 20), int(self.top - 20), int(self.w + 40), int(self.h + 40)), 1)
        text = self.font_win.render("OFF", True, (255, 0, 0))
        scale_rect = text.get_rect(
            center=(db.WIDTH // 2, db.HEIGHT // 2))
        db.screen.blit(text, scale_rect)
        pygame.display.flip()
        time.sleep(3)

    def timer_start(self):
        if not db.game:
            text = self.font_timer_game.render(str(db.seconds), True, (255, 255, 255))
            db.screen.blit(text, (db.WIDTH // 2 - 50, db.HEIGHT // 2 - 100))

    def run(self):
        while db.can_play:
            # print(self.clock.get_fps())
            db.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # control
            self.control((db.hand[0] * self.quotient_w, db.hand[1]))
            # draw
            self.draw()
            # ball movement
            self.ball_movement()
            self.ball_collision()
            # win, game over
            self.win_game_over()

            pygame.display.flip()
            self.clock.tick(db.fps)

    def delay(self):
        while not db.game:
            # print(self.clock.get_fps())
            db.screen.fill((0, 0, 0))
            self.draw()
            self.timer_start()
            pygame.display.flip()
            self.clock.tick(db.fps)
            # self.control()
