from copy import copy
from random import randint, random
from itertools import product

from simulation.vector2 import Vector2

def mix_list(list_):
    ln = len(list_)
    return [list_.pop(randint(0,ln-i-1)) for i in range(ln)]

def get_coord_combos(list1, list2):
    vectors = []
    for prd in product(list1, list2):
        vectors.append(Vector2(prd))
    return vectors

class Map:

    def __init__(self, size):
        self.__map = {}
        self.__count = {}
        self.size = size
        self.empty_cells = size.x*size.y


    def get(self, position):
        if self.is_empty(position):
            return None
        return self.__map[position]

    #get list of lists of entities for each type
    def get_entities(self, *entity_types):
        appropriate_entities = [[] for i in range(len(entity_types))]

        types_count = len(entity_types)

        for key in self.__map.keys():
            entity = self.get(key)
            for it in range(types_count):
                entity_type = entity_types[it]
                if issubclass(type(entity),entity_type):
                    appropriate_entities[it].append(entity)

        if types_count == 1:
            return appropriate_entities[0]
        return appropriate_entities

    def get_count(self, entity_type):
        if entity_type not in self.__count.keys():
            return 0
        return self.__count[entity_type]

    def is_empty(self, position):
        return position not in self.__map

    def add(self, entity, position):
        self.__map[position] = entity
        entity.set_position(position)
        entity.set_map(self)
        self.empty_cells -= 1

        entity_type = type(entity)
        if entity_type not in self.__count:
            self.__count[entity_type] = 1
        else: self.__count[entity_type] += 1

    def remove(self, entity_pos):
        if entity_pos not in self.__map.keys():
            return

        entity = self.__map.pop(entity_pos)
        self.__count[type(entity)]-=1
        self.empty_cells += 1

    def move(self, old_pos, new_pos):
        entity = self.get(old_pos)
        self.remove(old_pos)
        self.add(entity, new_pos)

    #check if position is in map bounds
    def is_valid_pos(self, pos):
        return  Vector2(0,0) <= pos < self.size

    def _get_surrounding_positions(self, anchor_pos):
        result = []
        range_ = (-1,0,1)
        for coord in get_coord_combos(range_, range_):

            current_pos = anchor_pos+coord

            if self.is_valid_pos(current_pos):
                result.append(current_pos)

        return result

    def get_neighbors(self, anchor_pos):
        neighbors = []

        surrounding_positions = self._get_surrounding_positions(anchor_pos)
        for current_pos in surrounding_positions:

            if not self.is_empty(current_pos):
                neighbors.append(self.get(current_pos))

        return neighbors

    def add_randomly(self, entity, count=1):
        if self.empty_cells == 0: return

        if count > self.empty_cells:
            count = self.empty_cells

        chance = float(count) / self.empty_cells

        while count > 0:
            for pos in get_coord_combos(
                range(self.size.x),
                range(self.size.y)):

                if not self.is_empty(pos): continue
                if not random() < chance: continue

                new_entity = copy(entity)
                self.add(new_entity, pos)

                count -= 1
                if count == 0: return

    #returns path to target if target_type specified
    #otherwise returns random path
    def build_path(self, pos_from, max_distance, target_type=type(None)):
        current_pos = pos_from
        came_from = {pos_from : None}
        queue = [pos_from]

        paths_to_empty = []

        while len(queue) != 0:
            current_pos = queue.pop(0)
            for coord in get_coord_combos(mix_list([-1,0,1]),
                                          mix_list([-1,0,1])):
                pos = current_pos + coord

                if pos in came_from: continue
                if pos in queue  : continue
                if not self.is_valid_pos(pos): continue
                if pos_from.distance(pos) > max_distance: continue

                entity_type = type(self.get(pos))
                if issubclass(entity_type, target_type):
                    cur = current_pos
                    path = []
                    while isinstance(cur, Vector2):
                        path.append(cur)
                        cur = came_from[cur]

                    path = path[::-1]

                    if target_type is not type(None):
                        return path

                    paths_to_empty.append(path)

                if self.is_empty(pos):
                    queue.append(pos)

                came_from[pos] = current_pos

        len_paths = len(paths_to_empty)
        if target_type is type(None) and \
                len_paths != 0:
            return paths_to_empty[randint(0, len_paths-1)]

        return None