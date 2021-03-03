from enemy import Enemy
from pygame.math import Vector2
from pygame import mixer
import pygame
import random


class Cat(Enemy):
    def __init__(self, game, speed):
        super().__init__(game, speed)
        self.icon = pygame.image.load('kotek.png')
        self.health = 5
        size = self.game.screen.get_size()
        while True:
            self.pos = Vector2(random.randint(0, size[0] - 80), size[1] / 3)
            self.rect = pygame.Rect(self.pos[0], self.pos[1], 64, 64)
            if self.rect.collidelist(self.game.rects) == -1:
                break

    def attack(self):
        dog = self.game.player
        dog.be_attacked()
        self.meow(True)

    def can_attack(self):
        dog = self.game.player
        if dog.is_close_to(self) and not dog.attacked:
            return True
        else:
            return False

    def draw(self):
        self.game.screen.blit(self.icon, self.pos)
        pygame.draw.rect(self.game.screen, (255, 0, 0), (self.pos[0] + self.health * 11, self.pos[1] - 15, 55 - self.health * 11 , 10))
        pygame.draw.rect(self.game.screen, (0, 255, 0), (self.pos[0], self.pos[1] - 15, self.health * 11 + 1, 10))
        pygame.draw.rect(self.game.screen, (0, 0, 255), (self.pos[0], self.pos[1], 64, 64), 2)


    @staticmethod
    def meow(attack=True):
        if attack:
            cat_sound = mixer.Sound('cat_scream.wav')
            cat_sound.set_volume(0.5)
            cat_sound.play()
        else:
            cat_sound = mixer.Sound('cat_meow_x.wav')
            cat_sound.play()