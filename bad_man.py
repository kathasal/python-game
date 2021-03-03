from enemy import Enemy
import pygame
from pygame.math import Vector2


class Dogcatcher(Enemy):
    def __init__(self, game, speed):
        super().__init__(game, speed)
        self.icon = [pygame.image.load('dogcatcher.png'), pygame.image.load('dogcatcherr.png')]
        self.r = False
        self.pos = Vector2(0, 54)

    def is_close_to(self):
        dog = self.game.player
        return pygame.Rect(self.pos[0], self.pos[1], 100, 64).colliderect(pygame.Rect(dog.pos[0], dog.pos[1], 64, 64))

    def catch(self):
        if self.is_close_to():
            self.game.game_over()

    def can_shot(self):
        dog = self.game.player
        return pygame.Rect(self.pos[0] - 40, self.pos[1] - 45, 200, 200).colliderect(pygame.Rect(dog.pos[0], dog.pos[1], 64, 64))

    def shot(self):
        dog = self.game.player
        if self.can_shot():
            if not dog.stop:
                dog.freeze()

    def draw(self):
        if self.r:
            self.game.screen.blit(self.icon[1], self.pos)
        else:
            self.game.screen.blit(self.icon[0], self.pos)
        pygame.draw.rect(self.game.screen, (0, 0, 255), (self.pos[0] - 40, self.pos[1] - 45, 200, 200), 2)
        pygame.draw.rect(self.game.screen, (255, 0, 0), (self.pos[0], self.pos[1], 100, 64), 2)

    def tick(self):
        super().tick()
        if self.d == Vector2(self.speed, 0):
            self.r = True
        elif self.d == Vector2(-self.speed, 0):
            self.r = False



