import random
from default_values import *

class Thing:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH-THING_WIDTH)
        self.y = 0
        self.w = THING_WIDTH
        self.h = THING_HEIGHT
        self.dx = random.randint(-1, 1)
        self.dy = 5

    def update(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy