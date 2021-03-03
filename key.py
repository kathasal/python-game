import pygame
from pygame import mixer

class Key():
    def __init__(self, game, pos=None):
        self.game = game
        self.icon = pygame.image.load('klucz.png')
        self.is_picked = False
        self.is_visible = False
        self.pos = pos

    def draw(self):
        if self.is_visible:
            self.game.screen.blit(self.icon, self.pos)

    def get_picked(self):
        self.is_picked = True
        self.is_visible = False
        key_sound = mixer.Sound('get_key.wav')
        key_sound.set_volume(1.0)
        key_sound.play()
