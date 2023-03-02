from player import Player
from thing import Thing
from default_values import *

class Game:
    def __init__(self):
        self.player = Player() # Se instancia el atributo player, como objeto de la clase Player
        self.thing_list = []
    
    def create_thing(self):
        thing = Thing() # Se instancia el objeto thing de la clase Thing
        self.thing_list.append(thing)
