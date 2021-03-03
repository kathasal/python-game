import pygame, sys
from dog import Dog
from cat import Cat
from bone import Bone
from cross import Cross
from key import Key
from bad_man import Dogcatcher
from puppy import Puppy
import random
from pygame import mixer


class Game():

    def __init__(self, num_cats, speed_cats, speed_dc, play=True):
        self.tps_max = 100.0
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Save the puppy!')
        self.clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.puppy = Puppy(self)
        self.rects = [pygame.Rect(0, 0, 350, 54), self.puppy.rect, pygame.Rect(800, 0, 40, 200),
                      pygame.Rect(800, 200, 200, 40), pygame.Rect(200, 600, 40, 120),
                      pygame.Rect(240, 600, 200, 40), pygame.Rect(1000, 500, 280, 40), pygame.Rect(1000, 540, 40, 100),
                      pygame.Rect(1000, 400, 40, 100), pygame.Rect(800, 400, 200, 40),
                      pygame.Rect(1070, 0, 240, 120),  pygame.Rect(0, 400, 200, 40), pygame.Rect(160, 200, 40, 200),
                      pygame.Rect(200, 200, 300, 40), pygame.Rect(460, 240, 40, 150)]
        self.player = Dog(self)
        self.proj = []
        self.cats = [Cat(self, speed_cats) for i in range(num_cats)]
        self.dogcatcher = Dogcatcher(self, speed_dc)
        self.bones = [Bone(self) for i in range(4)]
        self.crosses = [Cross(self) for i in range(5)]
        self.key = Key(self)
        self.ic = [pygame.image.load('heart.png'), pygame.image.load('kosc_m.png'),pygame.image.load('klucz_m.png')]
        self.crosses[random.randint(0, len(self.crosses)-1)].hide_key(self.key)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.instruct_f = pygame.font.Font('freesansbold.ttf', 16)
        self.over = 2

        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if self.over == 2:
                        self.over = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    for bone in self.bones:
                        if self.player.is_close_to(bone):
                            self.player.eat_bone(bone)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.bark()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and not self.player.stop:
                    for cross in self.crosses:
                        if self.player.is_close_to(cross):
                            self.player.start_time = pygame.time.get_ticks()
                            self.player.cross = cross
                    if not self.bones:
                        if pygame.Rect(self.player.pos[0] + 32, self.player.pos[1] + 32, 50, 50).colliderect(self.puppy.rect):
                            self.player.open()

            # ticking
            self.tps_delta += self.clock.tick() / 1000
            while self.tps_delta > 1 / self.tps_max:
                self.tps_delta -= 1 / self.tps_max
                if self.over == 0:
                    self.tick()


            # drawing
            self.screen.fill((0, 200, 0))
            self.screen.blit(pygame.image.load('bg.png'), (0,0))
            self.draw()
            pygame.display.flip()

    def tick(self):
        self.player.tick()
        self.puppy.cry()
        for p in self.proj:
            p.tick()
            for cat in self.cats:
                if pygame.Rect(p.x, p.y, 20, 20).colliderect(pygame.Rect(cat.pos[0], cat.pos[1], 40, 40)):
                    p.hit(cat)
        for cat in self.cats:
            if cat.health <= 0:
                cat.meow(False)
                self.cats.remove(cat)
            cat.tick()
            if cat.can_attack():
                cat.attack()
        if {self.player.is_close_to(cat) for cat in self.cats} == {False}:
            self.player.attacked = False
        self.dogcatcher.tick()
        self.dogcatcher.shot()
        self.dogcatcher.catch()
        if self.player.lives == 0 and self.over == 0:
            self.game_over()

    def draw(self):
        self.puppy.draw()
        for p in self.proj:
            p.draw()
        for bone in self.bones:
            bone.draw()
        for cross in self.crosses:
            cross.draw()
        self.key.draw()
        for cat in self.cats:
            cat.draw()
        self.player.draw()
        self.dogcatcher.draw()
        lives = self.font.render(' : ' + str(self.player.lives), True, (0, 0, 0))
        self.screen.blit(self.ic[0], (10, 10))
        self.screen.blit(lives, (40, 10))
        self.screen.blit(self.ic[1], (100, 10))
        self.screen.blit(self.font.render(' : ' + str(self.player.bones), True, (0, 0, 0)), (130, 10))
        self.screen.blit(self.ic[2], (190, 10))
        self.screen.blit(self.font.render(' : ' + str(self.player.key), True, (0, 0, 0)), (220, 10))

        self.screen.blit(self.instruct_f.render('Use arrows to move dog', True, (0, 0, 0)), (1082, 5))
        self.screen.blit(self.instruct_f.render('Press space to bark', True, (0, 0, 0)), (1082, 20))
        self.screen.blit(self.instruct_f.render('Press e to eat bone', True, (0, 0, 0)), (1082, 35))
        self.screen.blit(self.instruct_f.render('Press r to pick key', True, (0, 0, 0)), (1082, 50))
        self.screen.blit(self.instruct_f.render('Hold d to dig', True, (0, 0, 0)), (1082, 65))
        self.screen.blit(self.instruct_f.render('and then pres it', True, (0, 0, 0)), (1082, 80))
        self.screen.blit(self.instruct_f.render('until you save the pup!', True, (0, 0, 0)), (1082, 95))

        if self.over == -1:
            over_font = pygame.font.Font('freesansbold.ttf', 100)
            self.screen.blit(over_font.render('GAME OVER', True, (0, 0, 0)), (350, 300))
        elif self.over == 1:
            over_font = pygame.font.Font('freesansbold.ttf', 100)
            self.screen.blit(over_font.render('GAME WON', True, (0, 0, 0)), (350, 300))
        elif self.over == 2:
            pygame.draw.rect(self.screen, (200, 191, 231), (300, 150, 700, 500))
            self.screen.blit(self.font.render('INSTRUCTION', True, (0, 0, 0)), (350, 200))
            self.screen.blit(self.font.render('Use arrows to move dog, avoid cats', True, (0, 0, 0)), (360, 240))
            self.screen.blit(self.font.render('each contact with them takes one life.', True, (0, 0, 0)), (360, 280))
            self.screen.blit(self.font.render('Defend by barking on them (space)', True, (0, 0, 0)), (360, 320))
            self.screen.blit(self.font.render('You have to be strong - eat all bones (e).', True, (0, 0, 0)), (360, 360))
            self.screen.blit(self.font.render('Key is buried in place marked by cross,', True, (0, 0, 0)), (360, 400))
            self.screen.blit(self.font.render('Dig for 3 sec to uncover cross (hold d).', True, (0, 0, 0)), (360, 440))
            self.screen.blit(self.font.render('Then break the cage by pressing d.', True, (0, 0, 0)), (360, 480))
            self.screen.blit(self.font.render('Good luck', True, (0, 0, 0)), (360, 520))
            self.screen.blit(self.font.render('Press p to play', True, (0, 0, 0)), (400, 560))


    def game_over(self):
        self.over = - 1
        self.cats = []
        self.bones = []
        self.crosses = []
        self.player.start_time = None
        over_sound = mixer.Sound('game_over.wav')
        over_sound.set_volume(1.0)
        over_sound.play()

    def win(self):
        self.over = 1
        mixer.music.load('win.mp3')
        mixer.music.play()


if __name__ == '__main__':
    print('Welcome to \'Save the puppy!\' game')
    nc = int(input('Please choose number of Cat enemies: '))
    sc = float(input('Set their speed (your speed is 2): '))
    sd = float(input('Finally set speed of bad dog-catcher: '))
    print('Enjoy!')
    g = Game(nc, sc, sd)
