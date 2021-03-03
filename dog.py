import pygame
from pygame.math import Vector2
from projectile import Projectile
from pygame import mixer


class Dog():

    def __init__(self, game):
        self.game = game
        self.speed = 2
        size = self.game.screen.get_size()
        self.pos = Vector2(size[0]/ 2, size[1] / 2)
        self.icon = [pygame.image.load('piesel.png'), pygame.image.load('pieselr.png')]
        self.bones = 0
        self.key = False
        self.lives = 5
        self.attacked = False
        self.d = Vector2(1,0)
        self.start_time = None
        self.cross = None
        self.stop = False

    def tick(self):
        if not self.stop:
            #input
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT] and pygame.Rect(self.pos[0] + 1, self.pos[1], 64, 60).collidelist(self.game.rects) == -1 and self.pos[0] < 1220:
                self.pos += Vector2(self.speed, 0)
                self.d = Vector2(self.speed, 0)
            elif pressed[pygame.K_LEFT] and pygame.Rect(self.pos[0] - 1, self.pos[1], 64, 60).collidelist(self.game.rects) == -1 and self.pos[0] > 0:
                self.pos += Vector2(-self.speed, 0)
                self.d = Vector2(-self.speed, 0)
            elif pressed[pygame.K_UP] and pygame.Rect(self.pos[0], self.pos[1] - 1, 64, 60).collidelist(self.game.rects) == -1 and self.pos[1] > 0:
                self.pos += Vector2(0, - self.speed)
            elif pressed[pygame.K_DOWN] and pygame.Rect(self.pos[0], self.pos[1] + 1, 64, 60).collidelist(self.game.rects) == -1 and self.pos[1] < 664:
                self.pos += Vector2(0, self.speed)

            if self.game.key.is_visible and self.is_close_to(self.game.key) and pressed[pygame.K_r]:
                self.pick_key(self.game.key)

            if self.start_time is not None:
                if self.is_close_to(self.cross) and pressed[pygame.K_d]:
                    self.dig(self.cross)
                elif not self.is_close_to(self.cross) or not pressed[pygame.K_d]:
                    self.start_time = None
        else:
            time_since = pygame.time.get_ticks() - self.start_time
            if time_since > 3000:
                self.start_time = None
                self.stop = False

    def pick_key(self, key):
        key.get_picked()
        self.key = True

    def draw(self):
        if self.d == Vector2(- self.speed, 0):
            self.game.screen.blit(self.icon[0], self.pos)
        else:
            self.game.screen.blit(self.icon[1], self.pos)
        if self.start_time is not None:
            time_since = pygame.time.get_ticks() - self.start_time
            message = 'Time: ' + str(3 - time_since / 1000)[:4]
            if self.pos[0] - 20 < 0:
                self.game.screen.blit(self.game.font.render(message, True, (0, 0, 0)), (self.pos[0], self.pos[1] - 40))
            elif self.pos[0] - 20 > 1150 and self.pos[1] - 40 < 0:
                self.game.screen.blit(self.game.font.render(message, True, (0, 0, 0)), (self.pos[0] - 100, self.pos[1] + 80))
            elif self.pos[1] - 40 < 0:
                self.game.screen.blit(self.game.font.render(message, True, (0, 0, 0)), (self.pos[0] - 20, self.pos[1] + 80))
            elif self.pos[0] - 20 > 1150:
                self.game.screen.blit(self.game.font.render(message, True, (0, 0, 0)), (self.pos[0] - 100, self.pos[1] - 40))
            else:
                self.game.screen.blit(self.game.font.render(message, True, (0, 0, 0)), (self.pos[0] - 20, self.pos[1] - 40))
        pygame.draw.rect(self.game.screen, (255, 0, 0), (self.pos[0], self.pos[1], 64, 64), 2)

    def is_close_to(self, other):
        return pygame.Rect(self.pos[0], self.pos[1], 64, 64).colliderect(pygame.Rect(other.pos[0], other.pos[1], 64, 64))

    def eat_bone(self, bone):
        self.bones += 1
        bone.get_eaten()
        eat_sound = mixer.Sound('bite.wav')
        eat_sound.play()

    def dig(self, cross):
        time_since = pygame.time.get_ticks() - self.start_time
        if time_since > 3000:
            cross.dig_in()
            self.start_time = None
            self.cross = None

    def be_attacked(self):
        self.lives -= 1
        if self.attacked:
            self.attacked = False
        else:
            self.attacked = True

    def bark(self):
        if len(self.game.proj) < 5:
            w = Projectile(self.game, self.pos[0], self.pos[1], self.d[0])
            self.game.proj.append(w)
        bark_sound = mixer.Sound('deepbark.wav')
        bark_sound.play()

    def open(self):
        if self.key:
            self.game.puppy.cage_open()
            bark_sound = mixer.Sound('deepbark.wav')
            bark_sound.set_volume(0.5)
            bark_sound.play()

    def freeze(self):
        self.stop = True
        self.start_time = pygame.time.get_ticks()







