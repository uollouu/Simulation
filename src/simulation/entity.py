from abc import ABC, abstractmethod
from copy import *
from colorama import Back
import emoji

from random import *
from consts import *
from vector2 import *

SCOPE_TO_SPEED_RATIO = 3

class Entity(ABC):

    def __init__(self, map_=None, position=None):
        self.position = copy(position)
        self.map = map_

    @classmethod
    @property
    @abstractmethod
    def sprite(cls):
        raise NotImplementedError

    def set_map(self, map_):
        self.map = map_

    def set_position(self, position):
        self.position = copy(position)

    def kill(self):
        self.map.remove(self.position)





class Tree(Entity):
    sprite = Back.LIGHTGREEN_EX + " T " + Back.RESET

    def __init__(self, map_=None, position=None):
        super().__init__(map_, position)

class Grass(Entity):
    sprite = Back.GREEN + " G " + Back.RESET

    def __init__(self, nutrients, map_=None, position=None):
        super().__init__(nutrients, map_)
        self.nutrients = nutrients

class Rock(Entity):
    sprite = Back.RED + " R " + Back.RESET

    def __init__(self, map_=None, position=None):
        super().__init__(map_, position)


class Creature(Entity, ABC):

    def __init__(self, health, speed, scope=0, map_=None, position=None):
        super().__init__(map_, position)
        self.max_health = self.health = health
        self.speed = speed
        self.scope = scope
        if scope == 0: self.scope = self.speed * SCOPE_TO_SPEED_RATIO
        self._is_alive = True


    @abstractmethod
    def make_move(self):
        pass

    def move_to(self, new_position):
        self.map.move(self.position, new_position)

    def move_randomly(self):
        paths = self.map.find_target(self.position, self.scope)
        len_ = len(paths)
        if len_ == 0: return

        random_path = paths[randint(0,len_-1)]
        self.follow_path(random_path)

    def follow_path(self, path):
        if len(path) <= self.speed:
            self.move_to(path[-1])
        else:
            self.move_to(path[self.speed])

    def consume(self, entity, entity_nutrients):
        self.heal(entity_nutrients)

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
    sprite = Back.BLUE + " P " + Back.RESET

    def __init__(self, health, speed, attack_power, scope=0, map_=None, position=None):
        super().__init__(health, speed, scope, map_, position)
        self.attack_power = attack_power

    def attack(self, target):
        if target.health <= self.attack_power:
            self.consume(target, target.max_health)
        target.reduce_health(self.attack_power)


    def make_move(self):
        res = self.map.find_target(self.position, self.scope, Herbivore)

        if res is None:
            self.move_randomly()
            return

        target_pos, path = res
        self.follow_path(path)

        if self.position == path[-1]:
            target = self.map.get(target_pos)
            self.attack(target)


class Herbivore(Creature):
    sprite = Back.LIGHTYELLOW_EX + " H " + Back.RESET

    def __init__(self, health, speed, scope=0, map_=None, position=None):
        super().__init__(health, speed, scope, map_, position)

    def make_move(self):
        res = self.map.find_target(self.position, self.scope, Grass)

        if res is None:
            self.move_randomly()
            return

        target_pos, path = res

        self.follow_path(path)

        if self.position == path[-1]:
            target = self.map.get(target_pos)
            self.consume(target, target.nutrients)
            target.kill()








