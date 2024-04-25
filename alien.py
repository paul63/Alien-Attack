"""
Author Paul Brace April 2024
Alien class for Galaxians type space invaders game
"""

import pygame
import constants as const
from game_sprite import GameSprite
import math

# to_do make crossing aliens flap their wings.
# Maybe change colour for flying aliens

def path(p0, p1, p2, t):
    # return position on bezier curve based on t = 0 for start 1 = end
    px = p0[0] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[0] + p2[0] * t ** 2
    py = p0[1] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[1] + p2[1] * t ** 2
    return px, py

class Alien(GameSprite):
    # Create alien class
    # static variables
    moving = False
    start_speed = 3
    speed = start_speed
    # frames between setting a random alien flying
    fly_interval = 200
    fly_timer = fly_interval
    # counter to next crossing alien appearance
    special_alien_timer = 1

    # frames between wings moving
    FLAP_SPEED = 10
    alien_hit = pygame.mixer.Sound('sounds/strike.wav')
    normal_flap_0 = pygame.image.load('images/alien11.png')
    normal_flap_1 = pygame.image.load('images/alien12.png')
    special_flap_0 = pygame.image.load('images/alien01.png')
    special_flap_1 = pygame.image.load('images/alien02.png')

    def __init__(self, start_row, col_number, atype):
        # aType normal = standard alien in grid
        # cleft = moving from right to x at y of screen
        # else = moving x to right at y of screen
        self.atype = atype
        if atype == "normal":
            """ initialise at row and column """
            super().__init__(self.normal_flap_0, 0, 0)
            self.y = start_row * self.height
            self.x = 175 + col_number * self.width * 1.25
            self.dx = Alien.speed
            self.flap_0 = self.normal_flap_0
            self.flap_1 = self.normal_flap_1
        else:
            """ initialise for crossing """
            super().__init__(self.special_flap_0, 0, 0)
            self.flap_0 = self.special_flap_0
            self.flap_1 = self.special_flap_1
            if atype == "cleft":
                # special alien crossing right to left
                self.y = 40
                self.x = const.WIDTH
                self.dx = -Alien.speed
            else:
                # special alien crossing left to right
                self.y = 40
                self.x = 0
                self.dx = Alien.speed
        self.timer = Alien.FLAP_SPEED
        # alive set to false when alien hit
        self.alive = True
        # set variables used if actor flying
        self.start = 0
        self.end = 0
        self.mid = 0
        self.fly_delta = 0
        self.fly_pos = 0

    def update(self):
        """ check for image change and move if game in progress """
        if Alien.moving and self.alive:
            # if alien is flying will move following a bezier curve
            if self.atype == "flying":
                self.fly_pos += self.fly_delta
                self.x, self.y = path(self.start, self.mid, self.end, self.fly_pos)
                if self.y + self.height / 2 > const.HEIGHT:
                    self.done = True
            elif self.atype == "normal":
                self.x += self.dx
                if (self.x < self.width / 2 and self.dx < 0) or \
                   (self.x > const.WIDTH - self.width / 2 and self.dx > 0):
                    self.move_down()

            else:
                self.x += self.dx
                if (self.x < 0 - self.width and self.dx < 0) or \
                   (self.x > const.WIDTH + self.width and self.dx > 0):
                    self.done = True

        self.change_image()

    def move_down(self):
        """ used when reached end of screen move down and reverse direction """
        self.dx = -self.dx
        self.y += self.height // 2
        if self.y > const.HEIGHT + self.width / 2:
            self.done = True

    def hit(self):
        """ alien hit so change state - timer is for animation of alien """
        self.alien_hit.play()
        self.done = True
        self.timer = 0
        if self.atype == "normal":
            score = 10
        else:
            score = 50
        self.done = True
        return score

    def change_image(self):
        """ if still alive - if normal or flying change image each flap period
            if not alive animate explosion """
        if self.alive:
            self.timer -= 1
            if self.timer < 1:
                self.timer = Alien.FLAP_SPEED
                if self._image == self.flap_0:
                    self.set_image(self.flap_1)
                else:
                    self.set_image(self.flap_0)

    def start_flying(self, x, y):
        # set the alien flying on a bezier curve from current position to target position x:y
        # Ignore if already flying
        if self.atype == "flying":
            return
        self.atype = "flying"
        self.flap_0 = self.special_flap_0
        self.flap_1 = self.special_flap_1
        # Set control points
        self.start = (self.x, self.y)
        #self.end = (x, const.HEIGHT + 100)
        self.end = (x, y)
        if self.x < const.WIDTH // 2:
            # self.mid = (random.randint(1, 100), random.randint(1, 100))
            self.mid = (1, 1)
        else:
            self.mid = (const.WIDTH, 1)
            # self.mid = (random.randint(WIDTH - 100, WIDTH), random.randint(1, 100))
        # calculate distance to player
        self.fly_delta = 2 / math.sqrt(pow((x - self.x), 2) + pow((y - self.y), 2))
        self.fly_pos = 0

