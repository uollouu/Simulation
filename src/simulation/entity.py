from abc import ABC, abstractmethod
from copy import copy
from random import randint

from colorama import Back

#by default each creature's scope will be speed*ratio
SCOPE_TO_SPEED_RATIO = 3

#sprites
EMPTY_SPRITE     = Back.BLACK + " E " + Back.RESET

PREDATOR_SPRITE  = Back.BLUE + " P " + Back.RESET
HERBIVORE_SPRITE = Back.LIGHTYELLOW_EX + " H " + Back.RESET
GRASS_SPRITE     = Back.GREEN + " G " + Back.RESET
ROCK_SPRITE      = Back.RED + " R " + Back.RESET
TREE_SPRITE      = Back.LIGHTGREEN_EX + " T " + Back.RESET


class Entity(ABC):

    def __init__(self, map_=None, position=None):
        self.map = map_
        self.position = copy(position)

    @classmethod
    @property
    @abstractmethod
    def sprite(cls):
        raise NotImplementedError

    def set_map(self, map_):
        self.map = map_

    def set_position(self, position):
        if self.position is None:
            self.position = copy(position)
        else:
            self.position.set(position)

    def kill(self):
        self.map.remove(self.position)


class Tree(Entity):
    sprite = TREE_SPRITE

    def __init__(self, map_=None, position=None):
        super().__init__(map_, position)


class Grass(Entity):
    sprite = GRASS_SPRITE

    def __init__(self, nutrients, map_=None, position=None):
        super().__init__(map_, position)
        self.nutrients = nutrients


class Rock(Entity):
    sprite = ROCK_SPRITE

    def __init__(self, map_=None, position=None):
        super().__init__(map_, position)


class Creature(Entity, ABC):

    def __init__(self, health, speed, scope=0, map_=None, position=None):
        super().__init__(map_, position)
        self.max_health = self.health = health
        self.speed = speed
        self.scope = scope
        if scope == 0:
            self.scope = self.speed * SCOPE_TO_SPEED_RATIO

        self._is_alive = True

    @abstractmethod
    def make_move(self):
        pass

    def move_to(self, new_position):
        self.map.move(self.position, new_position)

    def move_randomly(self):
        random_path = self.map.build_path(self.position, self.scope)
        if random_path is not None:
            self.follow_path(random_path)

    def follow_path(self, path):
        self.move_to(path[min(self.speed, len(path)-1)])

    def reduce_health(self, points):
        self.health = max(0, self.health - points)
        if self.health == 0:
            self._is_alive = False
            self.kill()

    def heal(self, points):
        if not self.is_dead():
            self.health = min(self.max_health, self.health + points)

    def is_dead(self):
        return not self._is_alive


class Predator(Creature):
    sprite = PREDATOR_SPRITE

    def __init__(self, health, speed, attack_power, scope=0, map_=None, position=None):
        super().__init__(health, speed, scope, map_, position)
        self.attack_power = attack_power

    def attack(self, target):
        if target.health <= self.attack_power:
            self.heal(target.max_health)
        target.reduce_health(self.attack_power)

    def make_move(self):
        path = self.map.build_path(self.position, self.scope, Herbivore)

        if path is None:
            self.move_randomly()
            return

        self.follow_path(path)

        neighbors = self.map.get_neighbors(self.position)
        for i in neighbors:
            if type(i) == Herbivore:
                self.attack(i)

class Herbivore(Creature):
    sprite = HERBIVORE_SPRITE

    def __init__(self, health, speed, scope=0, map_=None, position=None):
        super().__init__(health, speed, scope, map_, position)

    def make_move(self):
        path = self.map.build_path(self.position, self.scope, Grass)

        if path is None:
            self.move_randomly()
            return

        self.follow_path(path)

        neighbors = self.map.get_neighbors(self.position)
        for i in neighbors:
            if type(i) == Grass:
                target = i
                self.heal(target.nutrients)
                target.kill()
