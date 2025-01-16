from abc import ABC, abstractmethod

from entity import *
from map import *

# Default entities
PREDATOR = Predator(100,3,20)
PREDATORS_COUNT = 5

HERBIVORE = Herbivore(100,2)
HERBIVORES_COUNT = 5
MIN_HERBIVORES_COUNT = 2

GRASS = Grass(30)
GRASS_COUNT = 5
MIN_GRASS_COUNT = 5

ROCK = Rock()
ROCKS_COUNT = 5

TREE = Tree()
TREES_COUNT = 5

class Action(ABC):

    def __init__(self, map_):
        self.map = map_

    @abstractmethod
    def perform(self):
        pass

class AddPredators(Action):

    def __init__(self, map_):
        super().__init__(map_)

    def perform(self, predator=PREDATOR,
                count = PREDATORS_COUNT):
        self.map.add_randomly(predator, count)


class AddHerbivores(Action):

    def __init__(self, map_):
        super().__init__(map_)

    def perform(self, herbivore=HERBIVORE,
                count=HERBIVORES_COUNT):
        self.map.add_randomly(herbivore, count)


class AddRocks(Action):

    def __init__(self, map_):
        super().__init__(map_)

    def perform(self, rock=ROCK,
                count=ROCKS_COUNT):
        self.map.add_randomly(rock, count)


class AddGrass(Action):

    def __init__(self, map_):
        super().__init__(map_)

    def perform(self, grass=GRASS,
                count=GRASS_COUNT):
        self.map.add_randomly(grass, count)


class AddTrees(Action):

    def __init__(self, map_):
        super().__init__(map_)

    def perform(self, tree=TREE,
                count=TREES_COUNT):
        self.map.add_randomly(tree, count)


class RunCreatures(Action):

    def __init__(self, map_):
        super().__init__(map_)

    def perform(self):
        creatures = self.map.get_entities(Creature)
        for creature in creatures:
            creature.make_move()


class HitAll(Action):

    def __init__(self, map_):
        super().__init__(map_)

    def perform(self, damage=TURN_DAMAGE):
        creatures = self.map.get_entities(Creature)
        for creature in creatures:
            creature.reduce_health(damage)


class AddOptionally(Action):

    def __init__(self, map_, entity, add_count, min_count):
        super().__init__(map_)
        self.min_count = min_count
        self.entity = entity
        self.add_count = add_count

    def perform(self):
        if self.map.get_count(type(self.entity)) < self.min_count:
            self.map.add_randomly(self.entity, self.add_count)


class HerbivoresAddOptionally(AddOptionally):

    def __init__(self, map_, herbivore=HERBIVORE,
                 add_count=HERBIVORES_COUNT,
                 min_count=MIN_HERBIVORES_COUNT):
        super().__init__(map_, herbivore, add_count, min_count)


class GrassAddOptionally(AddOptionally):

    def __init__(self, map_, grass=GRASS,
                 add_count=GRASS_COUNT,
                 min_count=MIN_GRASS_COUNT):
        super().__init__(map_, grass, add_count, min_count)


