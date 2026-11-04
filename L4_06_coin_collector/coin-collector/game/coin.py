"""
Coin: a static collectible circle. Drawn as a circle, hit-tested as a
bounding square around it.
"""

import pygame


class Coin:
    def __init__(self, x, y,value, color,radius=12):
        self.x = x
        self.y = y
        self.radius = radius
        self.value = value
        self.color = color

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
