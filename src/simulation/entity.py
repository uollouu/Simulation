from abc import ABC, abstractmethod
from copy import copy

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

    @abstractmethod
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

    def get_neighbors(self):
        return self.map.get_neighbors(self.position)

    def kill(self):
        self.map.remove(self.position)


class Tree(Entity):
    sprite = TREE_SPRITE

    def __init__(self, map_=None, position=None):
        super().__init__(map_, position)


class Rock(Entity):
    sprite = ROCK_SPRITE

    def __init__(self, map_=None, position=None):
        super().__init__(map_, position)


class Food(ABC):

    @abstractmethod
    def __init__(self, nutrients : int):
        self.nutrients = nutrients


class Grass(Entity, Food):
    sprite = GRASS_SPRITE

    def __init__(self, nutrients, map_=None, position=None):
        Entity.__init__(self, map_, position)
        Food.__init__(self, nutrients)


class Creature(Entity, Food, ABC):

    @abstractmethod
    def __init__(self, health, speed, scope=0, map_=None, position=None):
        Entity.__init__(self, map_, position)
        Food.__init__(self, health)
        self.max_health = self.health = health
        self.speed = speed
        self._is_alive = True
        self.scope = scope

        if self.scope == 0:
            self.scope = self.speed * SCOPE_TO_SPEED_RATIO

    @classmethod
    @property
    @abstractmethod
    def target_type(cls):
        raise NotImplementedError

    @abstractmethod
    def interact_with_target(self, target):
        pass

    def make_move(self):
        self.roam()

        target = self.get_target_neighbor()

        if target:
            self.interact_with_target(target)

    def get_target_neighbor(self):
        neighbors = self.get_neighbors()
        for entity in neighbors:
            if type(entity) == self.target_type:
                return entity
        return None

    def roam(self):
        path = self.map.build_path(self.position, self.scope, self.target_type)

        if path:
            self.follow_path(path)
        else:
            self.move_randomly()

    def move_to(self, new_position):
        self.map.move(self.position, new_position)

    def move_randomly(self):
        random_path = self.map.build_path(self.position, self.scope)
        if random_path:
            self.follow_path(random_path)

    def follow_path(self, path):
        self.move_to(path[min(self.speed, len(path)-1)])

    def reduce_health(self, points):
        self.health = max(0, self.health - points)
        if self.health == 0:
            self.kill()

    def heal(self, points):
        if not self.is_dead():
            self.health = min(self.max_health, self.health + points)

    def consume(self, target):
        self.heal(target.nutrients)
        target.kill()

    def kill(self):
        self.health = 0
        self._is_alive = False
        super(Creature, self).kill()

    def is_dead(self):
        return not self._is_alive


class Herbivore(Creature):
    sprite = HERBIVORE_SPRITE
    target_type = Grass

    def __init__(self, health, speed, scope=0, map_=None, position=None):
        super().__init__(health, speed, scope, map_, position)

    def interact_with_target(self, target):
        self.consume(target)


class Predator(Creature):
    sprite = PREDATOR_SPRITE
    target_type = Herbivore

    def __init__(self, health, speed, attack_power, scope=0, map_=None, position=None):
        super().__init__(health, speed, scope, map_, position)
        self.attack_power = attack_power

    def interact_with_target(self, target):
        if target.health <= self.attack_power:
            self.consume(target)
        else:
            target.reduce_health(self.attack_power)