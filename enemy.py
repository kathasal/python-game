import pygame
from pygame.math import Vector2
import random


class Enemy():
    def __init__(self, game, speed):
        self.game = game
        size = self.game.screen.get_size()
        self.leng = random.randrange(1, min(size))
        self.speed = speed
        self.d = random.choice([Vector2(0, self.speed), Vector2(0, -self.speed), Vector2(self.speed, 0), Vector2(-self.speed, 0)])

    def tick(self):
        self.pos += self.d
        if self.pos[0] <= 0 or self.pos[0] >= 1200 or self.pos[1] <= 0 or self.pos[1] >= 660:
            self.pos -= self.d
            self.leng = random.randrange(1, 600)
            self.d = random.choice([Vector2(0, self.speed), Vector2(0, -self.speed), Vector2(self.speed, 0), Vector2(-self.speed, 0)])
        if pygame.Rect(self.pos[0], self.pos[1], 64, 64).collidelist(self.game.rects) != -1:
            self.pos -= self.d
            self.leng = random.randrange(1, 600)
            self.d = random.choice([Vector2(0, self.speed), Vector2(0, -self.speed), Vector2(self.speed, 0), Vector2(-self.speed, 0)])
        self.leng -= 1
        if self.leng < 0:
            self.leng = random.randrange(1, 600)
            self.d = random.choice([Vector2(0, self.speed), Vector2(0, -self.speed), Vector2(self.speed, 0), Vector2(-self.speed, 0)])


