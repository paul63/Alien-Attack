"""
Author Paul Brace April 2024
Star class used to produce a star field where you are flying forward
for Galaxians type space invaders game
"""

import random
import constants as const

star_list = []

def initialize_stars():
    """creates a new starfield"""
    if len(star_list) == 0:
        for x in range(const.NUMSTARS):
            star = Star()
            # get a random number from 0 to half screen width
            steps = random.randint(0, int(const.WIDTH / 2))
            # move star to a random starting point along its direction
            star.x += star.dx * steps
            star.y += star.dx * steps
            # velocity increases as moves to edge of screen so
            # adjust velocity based on the random starting point
            star.dx *= steps * 0.09
            star.dy *= steps * 0.09
            star_list.append(star)

def clear_stars():
    while len(star_list) > 0:
        star_list.pop()

def move_stars(screen):
    for star in star_list:
        star.move()
        star.draw(screen)

class Star:
    # create star class
    def __init__(self):
        """ initialise star at center and with random direction and speed """
        self.dx = 0     # Speed of movement
        self.dy = 0     # Speed of movement
        self.x = 0      # x position on screen
        self.y = 0      # y position on screen
        self.setup()

    def setup(self):
        """ set random direction and speed """
        self.dx = (random.random() - 0.5) * 2
        self.dy = (random.random() - 0.5) * 2
        self.x = const.WIDTH / 2
        self.y = const.HEIGHT / 2

    def move(self):
        """ move star and increase speed.
            If reached edge of screen then reinitialise """
        self.x += self.dx
        self.y += self.dy
        # if star has reached the edge of the screen then reinitialize the star
        if not 0 <= self.x <= const.WIDTH or not 0 <= self.y <= const.HEIGHT:
            self.setup()
        else:
            # increase the velocity of the star
            self.dx *= 1.01
            self.dy *= 1.01

    def draw(self, screen):
        """ draw star by setting pixel """
        # pos = (int(self.x), int(self.y))
        screen.set_at((int(self.x), int(self.y)), 'white')
