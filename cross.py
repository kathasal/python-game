import pygame
from pygame.math import Vector2
import random


class Cross():

    def __init__(self, game):
        self.game = game
        size = self.game.screen.get_size()
        while True:
            self.pos = Vector2(random.randint(0, size[0] - 60), random.randint(0, size[1] - 60))
            self.rect = pygame.Rect(self.pos[0], self.pos[1], 40, 40)
            if self.rect.collidelist(self.game.rects) == -1:
                break
        self.is_empty = True
        self.icon = pygame.image.load('red_cross.png')
        self.key = None

    def hide_key(self, key):
        self.is_empty = False
        self.key = key
        self.key.pos = self.pos

    def dig_in(self):
        self.game.crosses.remove(self)
        if self.key is not None:
            self.key.is_visible = True

    def draw(self):
        self.game.screen.blit(self.icon, self.pos)

