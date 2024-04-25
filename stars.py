"""
Author Paul Brace April 2024
Star class use to produce a star field where you are flying upwards
for Galaxians type space invaders game
"""

import pygame.draw
import random
import constants as const

star_list = []

def initialize_stars():
    """creates a new starfield"""
    if len(star_list) == 0:
        for x in range(const.NUMSTARS):
            star = Star(
                random.randint(10, const.WIDTH - 10),
                random.randint(0, const.HEIGHT),
                random.randint(1, 2)
            )
            star_list.append(star)

def clear_stars():
    star_list.clear()

def move_stars(screen):
    for star in star_list:
        star.move()
        star.draw(screen)

class Star:
    # create star class
    def __init__(self, x, y, radius):
        """ initialise star at center and with random direction and speed """
        self.dy = 0.5     # Speed of movement
        self.x = x      # x position on screen
        self.y = y      # y position on screen
        self.radius = radius

    def move(self):
        """ move star and increase speed.
            If reached edge of screen then reinitialise """
        self.y += self.dy
        # if star has reached the edge of the screen then reinitialize the star
        if self.y > const.HEIGHT:
            self.y = 0

    def draw(self, screen):
        """ draw star by setting pixel """
        # pos = (int(self.x), int(self.y))
        pygame.draw.circle(screen, 'white', (self.x, self.y), self.radius)
