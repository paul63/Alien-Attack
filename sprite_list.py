"""
Author Paul Brace April 2024
SpriteList class for Galaxians type space invaders game
"""

class SpriteList():
    def __init__(self):
        self.list = []

    def add(self, item):
        self.list.append(item)


    def draw(self,screen):
        for item in self.list:
            item.draw(screen)

    def number(self):
        return len(self.list)

    def clear_done(self):
        for item in self.list:
            if item.done:
                self.list.remove(item)

    def clear_all(self):
        self.list.clear()
