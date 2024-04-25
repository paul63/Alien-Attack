"""
Author Paul Brace April 2024
Missile class for Galaxians type space invaders game
"""

import pygame
from game_sprite import GameSprite
import constants as const

class Missile(GameSprite):
    # set initial alien bomb interval - reduced each clear to increase the number of bombs
    start_bomb_interval = 40
    bomb_interval = start_bomb_interval
    bomb_timer = bomb_interval
    # speed will be increased for subsequent waves
    start_bomb_speed = 3
    bomb_speed = start_bomb_speed
    bullet_speed = 12
    bullet_image = pygame.image.load('images/bullet.png')
    bomb_image = pygame.image.load('images/bomb.png')
    bullet_released = pygame.mixer.Sound('sounds/bullet.wav')

    def __init__(self, x, y, direction):
        """ initialise bullet and set direction - up if player missile down if a bomb"""
        self.up = direction == 'up'
        if self.up:
            super().__init__(self.bullet_image, x, y)
        else:
            super().__init__(self.bomb_image, x, y)


    def update(self):
        """ move up or down  """
        if self.up:
            self.y -= self.bullet_speed
            if self.y < self.height / 2:
                self.done = True
        else:
            self.y += self.bomb_speed
            if self.y > const.HEIGHT + self.height / 2:
                self.done = True

    def bullet_sound(self):
        self.bullet_released.play()