from .vector2 import Vector2
from .sprites import get_sprite

class Matrix:

    def __init__(self, size):
        self.size = size
        self.pointer = Vector2(0,0)
        self.matrix = ["" for row in range(self.size.y)]

    def clear(self):
        for row in range(self.size.y):
            self.matrix[row] = ""

    #add cell at pointer position
    def add(self,cell):
        self.matrix[self.pointer.y] += cell
        self.pointer.x +=1
        if self.pointer.x >= self.size.x:
            self.pointer.x = 0
            self.pointer.y += 1

    def print(self):
        for y in range(self.size.y):
            print(self.matrix[y])

    def clear_pointer(self):
        self.pointer = Vector2(0,0)


class Renderer:

    def __init__(self, map_):
        self.map = map_
        self.matrix = Matrix(map_.size)

    def display(self):
        print()
        self.render_map()
        self.matrix.print()
        self.matrix.clear()
        print()

    def get_rendered_cell(self, position):
        entity = self.map.get(position)
        cell = get_sprite(entity)
        return cell

    def render_map(self):
        map_ = self.map
        for y in range(map_.size.y):
            for x in range(map_.size.x):
                position = Vector2(x,y)
                self.matrix.add(self.get_rendered_cell(position))
        self.matrix.clear_pointer()