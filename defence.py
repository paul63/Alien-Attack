"""
Author Paul Brace April 2024
Defence class for Galaxians type space invaders game
"""
from game_sprite import GameSprite
import pygame

class Defence(GameSprite):
    defence_hit = pygame.mixer.Sound('sounds/strike.wav')
    rock_start_image = pygame.image.load("images/defence3.png")

    # defence boulder class
    def __init__(self, x, y):
        """ initialise defence in position pos x:y"""
        super().__init__(self.rock_start_image, x, y)
        self.timer = 0
        # exploding is set to true when hit
        self.exploding = False
        # number of times hit
        self.damage = 0
        # True when hit for 1 update
        self.just_hit = False

    def hit(self):
        """ defence hit so change state - timer is for animation of explosion """
        self.defence_hit.play()
        self.timer = 0
        self.damage += 1
        self.just_hit = True

    def update(self):
        # if just been hit the display next image in sequence or remove if 4th hit
        if self.just_hit:
            if self.damage < 4:
                self.set_image(pygame.image.load("images/defence" + str(3 - self.damage) + ".png"))
                self.exploding = True
                self.just_hit = False
            else:
                self.done = True
        if self.exploding:
            self.timer += 1
            if self.timer > 24:
                self.exploding = False

