from .vector2 import *
from .entity import *

TURNS_CD = 0.3 #time between each map turn
TURN_DAMAGE = 3 #damage to entities per turn

DEFAULT_MAP_SIZE = Vector2(40,20)

# Default entities and their counts when add
###
PREDATOR = Predator(100,2,34)
PREDATORS_COUNT = 7

HERBIVORE = Herbivore(100,1)
HERBIVORES_COUNT = 10
MIN_HERBIVORES_COUNT = 2

GRASS = Grass(35)
GRASS_COUNT = 50
MIN_GRASS_COUNT = 20

ROCK = Rock()
ROCKS_COUNT = 200

TREE = Tree()
TREES_COUNT = 50
###