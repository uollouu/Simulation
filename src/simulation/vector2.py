class Vector2:

    def __init__(self, *args):
        self.x : int = -1
        self.y : int = -1
        self.set(*args)

    #args is either Vector2 or 2 ints
    def set(self, *args):
        if len(args) == 1:
            vector = args[0]

            if not isinstance(vector, Vector2):
                return NotImplemented

            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2:
            x, y = args[0:2]

            if not(isinstance(x,int) and isinstance(y,int)):
                return NotImplemented

            self.x = args[0]
            self.y = args[1]
        else:
            return NotImplemented

    def distance(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return max(abs(self.x-other.x), abs(self.y-other.y))

    def __add__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return Vector2(self.x+other.x, self.y+other.y)

    def __hash__(self):
        return hash((self.x,self.y))

    def __iter__(self):
        return iter([self.x,self.y])

    def __eq__(self,other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}; {self.y})"

    def __lt__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x < other.x and self.y < other.y

    def __le__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x <= other.x and self.y <= other.y

    def __gt__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x > other.x and self.y > other.y

    def __ge__(self,other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x >= other.x and self.y >= other.y
