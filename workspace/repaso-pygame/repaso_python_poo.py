from player import Player
from thing import Thing
from game import Game

g = Game()
print(len(g.thing_list))
g.create_thing()
print(len(g.thing_list))