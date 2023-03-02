from default_values import *

class Player:
    def __init__(self): # Metodo constructor de la clase Player
        # Es el que se llama cuando se instancia un objeto de la clase
        self.x = 0
        self.y = 0
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.dx = 0
        self.dy = 0
    
    def update(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def jump(self):
        self.dy = -10

    def turn_left(self):
        self.dx = -5

    def turn_right(self):
        self.dx = 5