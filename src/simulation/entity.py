from abc import ABC, abstractmethod
from copy import copy
from typing import ClassVar, Protocol

#by default each creature's scope will be speed*ratio
SCOPE_TO_SPEED_RATIO = 3


class Entity(ABC):

    def __init__(self, map_=None, position=None):
        self.map = map_
        self.position = copy(position)

    def set_map(self, map_):
        self.map = map_

    def set_position(self, position):
        if self.position is None:
            self.position = copy(position)
        else:
            self.position.set(position)

    def get_neighbors(self) -> list[object]:
        return self.map.get_neighbors(self.position)

    def kill(self):
        self.map.remove(self.position)


class Tree(Entity):

    def __init__(self, map_=None, position=None):
        super().__init__(map_, position)


class Rock(Entity):

    def __init__(self, map_=None, position=None):
        super().__init__(map_, position)


class Food(Protocol):
    nutrients : int


class Grass(Entity, Food):

    def __init__(self, nutrients, map_=None, position=None):
        super().__init__(map_, position)
        self.nutrients = nutrients


class Creature(Entity, Food):

    def __init__(self, health, speed, scope=0, map_=None, position=None):
        super().__init__(map_, position)
        self.max_health = self.health = self.nutrients = health
        self.speed = speed
        self._is_alive = True

        self.scope = scope

        if self.scope == 0:
            self.scope = self.speed * SCOPE_TO_SPEED_RATIO

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
            if self.is_target(entity):
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

    def is_target(self, entity):
        return type(entity) == self.target_type

    def is_dead(self):
        return not self._is_alive


class Herbivore(Creature):
    target_type : ClassVar[object] = Grass

    def __init__(self, health, speed, scope=0, map_=None, position=None):
        super().__init__(health, speed, scope, map_, position)

    def interact_with_target(self, target):
        self.consume(target)


class Predator(Creature):
    target_type : ClassVar[object] = Herbivore

    def __init__(self, health, speed, attack_power, scope=0, map_=None, position=None):
        super().__init__(health, speed, scope, map_, position)
        self.attack_power = attack_power

    def interact_with_target(self, target):
        if target.health <= self.attack_power:
            self.consume(target)
        else:
            target.reduce_health(self.attack_power)