import pygame


class Projectile():
    def __init__(self, game, x, y, d):
        self.x = x
        self.y = y
        self.game = game
        self.d = d
        self.icon = pygame.image.load('wave.png')

    def draw(self):
        self.game.screen.blit(self.icon, (self.x, self.y))

    def tick(self):
        self.x += self.d
        if self.x < 0 or self.x > 1280:
            self.game.proj.remove(self)

    def hit(self, cat):
        self.game.proj.remove(self)
        cat.health -= 1
        cat.meow(False)

