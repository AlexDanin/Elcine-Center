import pygame
from random import randrange as rnd
from DataBase import *
from PyGameClass import *
import keyboard

start = Start()


class Arcanoid:
    def __init__(self):
        # paddle settings
        self.paddle_w = 330
        self.paddle_h = 35
        self.paddle_speed = 15
        self.paddle = pygame.Rect(WIDTH // 2 - self.paddle_w // 2, HEIGHT - self.paddle_h - 10, self.paddle_w,
                                  self.paddle_h)
        # ball settings
        self.ball_radius = 20
        self.ball_speed = 6
        self.ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.ball = pygame.Rect(rnd(self.ball_rect, WIDTH - self.ball_rect), HEIGHT // 2, self.ball_rect,
                                self.ball_rect)
        self.dx, self.dy = 1, -1
        # blocks settings
        self.block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
        self.color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

    def draw(self):
        [pygame.draw.rect(start.sc, self.color_list[color], block) for color, block in enumerate(self.block_list)]
        pygame.draw.rect(start.sc, pygame.Color('darkorange'), self.paddle)
        pygame.draw.circle(start.sc, pygame.Color('white'), self.ball.center, self.ball_radius)

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
        if self.ball.centerx < self.ball_radius or self.ball.centerx > WIDTH - self.ball_radius:
            self.dx = -self.dx
        # collision top
        if self.ball.centery < self.ball_radius:
            self.dy = -self.dy
        # collision paddle
        if self.ball.colliderect(self.paddle) and self.dy > 0:
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, self.ball, self.paddle)
        # collision blocks
        hit_index = self.ball.collidelist(self.block_list)
        if hit_index != -1:
            hit_rect = self.block_list.pop(hit_index)
            hit_color = self.color_list.pop(hit_index)
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, self.ball, hit_rect)
            # special effect
            hit_rect.inflate_ip(self.ball.width * 3, self.ball.height * 3)
            pygame.draw.rect(start.sc, hit_color, hit_rect)
            start.fps += 2

    def control(self):
        # self.paddle.left = num * 100
        # key = keyboard.is_pressed('Esc')
        if keyboard.is_pressed('Left') and self.paddle.left > 0:
            self.paddle.left -= self.paddle_speed
        if keyboard.is_pressed('Right') and self.paddle.right < WIDTH:
            self.paddle.right += self.paddle_speed
        # print(key[pygame.K_LEFT], key[pygame.K_RIGHT], self.paddle.left, self.paddle.right)

    def win_game_over(self):
        if self.ball.bottom > HEIGHT:
            print('GAME OVER!')
            exit()
        elif not len(self.block_list):
            print('WIN!!!')
            exit()

    def run(self):
        # control
        # self.control(8)
        # draw
        self.draw()
        # ball movement
        self.ball_movement()
        self.ball_collision()
        # win, game over
        self.win_game_over()