import unittest
from pygame.math import Vector2
from game import Game
from dog import Dog
from enemy import Enemy
from key import Key


class Test(unittest.TestCase):
    def setUp(self):
        self.test_game = Game(3, 1, 1.5, False)

    def test_input(self):
        self.assertIsInstance(self.test_game.player, Dog)
        self.assertEqual(len(self.test_game.cats), 3)
        self.assertEqual(self.test_game.cats[1].speed, 1)
        self.assertEqual(self.test_game.dogcatcher.speed, 1.5)
        self.assertIsInstance(self.test_game.key, Key)

    def test_bone_eating(self):
        dog = self.test_game.player
        self.assertEqual(dog.bones, 0)
        self.assertEqual(len(self.test_game.bones), 4)
        while self.test_game.bones:
            bone = self.test_game.bones[0]
            dog.eat_bone(bone)
            self.assertNotIn(bone, self.test_game.bones)
        self.assertEqual(dog.bones, 4)
        self.assertFalse(self.test_game.bones)

    def test_enemy_ticking(self):
        cat = self.test_game.cats[0]
        self.assertIsInstance(cat, Enemy)
        cat.pos = Vector2(0, 500)
        cat.leng = 50
        cat.d = Vector2(cat.speed, 0)
        for _ in range(50):
            cat.tick()
        self.assertEqual(cat.pos, Vector2(cat.speed * 50, 500))

    def test_cat_attack(self):
        dog = self.test_game.player
        cat = self.test_game.cats[0]
        self.assertFalse(dog.is_close_to(cat))
        dog.pos = Vector2(50, 500)
        cat.pos = Vector2(80, 500)
        self.assertTrue(dog.is_close_to(cat))
        self.assertTrue(cat.can_attack())
        self.assertEqual(dog.lives, 5)
        self.assertFalse(dog.attacked)
        cat.attack()
        self.assertTrue(dog.attacked)
        self.assertEqual(dog.lives, 4)
        dog.pos = Vector2(0, 600)
        self.test_game.tick()
        self.assertFalse(dog.attacked)

    def test_barking_and_proj(self):
        dog = self.test_game.player
        self.assertFalse(self.test_game.proj)
        dog.pos = Vector2(100, 500)
        dog.d = Vector2(-1,0)
        dog.bark()
        self.assertEqual(len(self.test_game.proj), 1)
        for _ in range(10):
            dog.bark()
        self.assertEqual(len(self.test_game.proj), 5)
        cat = self.test_game.cats[0]
        cat.pos = Vector2(0, 500)
        proj = self.test_game.proj[0]
        proj.x = 40
        self.assertEqual(cat.health, 5)
        self.test_game.tick()
        self.assertEqual(cat.health, 4)
        self.assertNotIn(proj, self.test_game.proj)
        for _ in range(60):
            self.test_game.proj[0].tick()
        self.test_game.tick()
        self.assertEqual(cat.health, 3)
        for _ in range(3):
            for _ in range(60):
                self.test_game.proj[0].tick()
            self.test_game.tick()
        self.assertFalse(self.test_game.proj)
        self.assertNotIn(cat, self.test_game.cats)

    def test_puppy(self):
        dog = self.test_game.player
        dog.pick_key(self.test_game.key)
        dog.open()
        self.assertEqual(self.test_game.puppy.cage, 19)
        for _ in range(19):
            dog.open()
        self.test_game.puppy.go_out()
        self.assertEqual(self.test_game.over, 1)

    def test_dogcatcher(self):
        dc = self.test_game.dogcatcher
        dog = self.test_game.player
        dc.pos = Vector2(0, 500)
        dog.pos = Vector2(150, 500)
        self.assertTrue(dc.can_shot())
        self.assertFalse(dog.stop)
        dc.shot()
        self.assertTrue(dog.stop)
        dc.pos = Vector2(120, 500)
        self.assertTrue(dc.is_close_to())
        dc.catch()
        self.assertEqual(self.test_game.over, -1)


if __name__ == "__main__":
    unittest.main()
