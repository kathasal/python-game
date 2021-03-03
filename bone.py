import pygame
import random
from pygame.math import Vector2


class Bone():
    def __init__(self, game):
        self.game = game
        size = self.game.screen.get_size()
        while True:
            self.pos = Vector2(random.randint(0, size[0]-60), random.randint(0, size[1]-60))
            self.rect = pygame.Rect(self.pos[0], self.pos[1], 40, 40)
            if self.rect.collidelist(self.game.rects) == -1:
                break
        self.icon = pygame.image.load('kosc.png')

    def draw(self):
        self.game.screen.blit(self.icon, self.pos)

    def get_eaten(self):
        self.game.bones.remove(self)
