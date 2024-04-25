"""
Author Paul Brace April 2024
Player class for Galaxians type space invaders game
"""

import pygame
import constants as const
from game_sprite import GameSprite

class Player(GameSprite):
    # create player class
    # Interval between allowed firing
    RELOAD_TIME = 20
    player_hit = pygame.mixer.Sound('sounds/lifeLost.wav')
    player_image = pygame.image.load('images/player.png')

    def __init__(self, ):
        """ initialise positioned bottom center """
        super().__init__(self.player_image, const.WIDTH / 2, const.HEIGHT - 20)
        # When the player shoots, this is set to RELOAD_TIME - it then counts
        # down - when it reaches zero the player can shoot again
        # Also used to display player hit image for a few seconds
        self.timer = -1
        # alive is set to false when player hit
        self.alive = True
        # done tells main update to delete the object
        self.done = False

    def hit(self):
        """ player hit so set state and reduced lives
            timer is for animation of explosion """
        self.player_hit.play()
        self.alive = False
        self.timer = -1

    def reset(self):
        self.x = const.WIDTH / 2
        self.y = const.HEIGHT - 20
        self.alive = True
        self.done = False
        self.timer = -1

    def update(self):
        """ check if a key has been pressed and act accordingly
            count timer for firing interval
            if player presses space then returns True """
        fire = ""
        if self.alive:
            # loop 3 times to speed up movement but stop immediately key released
            for i in range(3):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and self.x > 0:
                    self.x -= 1
                if keys[pygame.K_RIGHT] and self.x < const.WIDTH:
                    self.x += 1
                if keys[pygame.K_SPACE]:
                    fire = "fire"
            self.timer -= 1
        else:
            self.timer += 1
            if self.timer > const.DELAY * 2:
                self.done = True
        return fire
    def draw(self, screen):
        if self.alive:
            super().draw(screen)
