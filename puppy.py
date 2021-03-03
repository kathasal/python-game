import pygame
from pygame.math import Vector2
import random
from pygame import mixer


class Puppy():
    def __init__(self, game):
        self.icon = pygame.image.load('puppy.png')
        self.game = game
        self.pos = Vector2(1160, 600)
        self.rect = pygame.Rect(1160, 600, 120, 120)
        self.cage = 20

    def draw(self):
        self.game.screen.blit(self.icon, self.pos)
        if self.cage > 0:
            message = 'Cage: ' + str(self.cage)
            self.game.screen.blit(self.game.font.render(message, True, (0, 0, 0)), (self.pos[0] - 20, self.pos[1] - 40))

    @staticmethod
    def cry():
        if random.random() < 0.0005:
            cry_sound = mixer.Sound('dog_puppy.wav')
            cry_sound.play()

    def cage_open(self):
        self.cage -= 1
        if self.cage == 0:
            self.go_out()
            self.game.rects.remove(self.rect)

    def go_out(self):
        self.icon = pygame.image.load('pup1.png')
        happy_sound = mixer.Sound('dog_bark5.wav')
        happy_sound.play()
        self.game.win()