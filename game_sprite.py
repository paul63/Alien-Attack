"""
Author Paul Brace April 2024
Base object for game sprites
"""

import pygame
import math

class GameSprite():
    # Base object for game sprites
    def __init__(self, image, x, y):
        """ initialise object """
        self._image = image
        self.width = self._image.get_width()
        self.height = self._image.get_height()
        #self.rect = self._image.get_bounding_rect()
        self.x = x
        self.y = y
        # Amount to move on an update
        self.dx = 0
        self.dy = 0
        # Done is used to indicate that the object is finished with and can be deleted
        self.done = False

    def get_image(self):
        return self._image

    def set_image(self, value):
        self._image = value
        self.width = self._image.get_width()
        self.height = self._image.get_height()
        #self.rect = self._image.get_bounding_rect()

    def update(self):
        """ move object dx and dy """
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        """ draw on screen - x,y is center of image """
        screen.blit(self._image, (self.x - self.width / 2, self.y - self.height / 2))

    def collide_rect(self, object):
        '''
        :param object:
        :return: True if the rectangles of both objects collide
        '''
        if abs(abs(self.x) - abs(object.x)) < self.width / 2 + object.width / 2 \
                and abs(abs(self.y) - abs(object.y)) < self.height / 2 + object.height / 2:
            return True
        else:
            return False

    def collide_circle(self, object):
        '''
        :param object:
        :return: True if the distance between self and the object
        is < the sum of half the widths of the objects. I.e intersection of
        two imaginary circles with a radius of half the width of the objects
        '''
        if math.dist((self.x, self.y), (object.x, object.y)) \
                < self.width / 2 + object.width / 2:
            return True
        else:
            return False



