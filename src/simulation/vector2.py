class Vector2:

    def __init__(self,x=-1,y=-1):
        self.x = x
        self.y = y

    def distance(self, other):
        return max(abs(self.x-other.x), abs(self.y-other.y))

    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+other.y)

    def __hash__(self):
        return hash((self.x,self.y))

    def __iter__(self):
        return iter([self.x,self.y])

    def __eq__(self,vector2):
        return self.x == vector2.x and self.y == vector2.y

    def __str__(self):
        return f"({self.x}; {self.y})"

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __ge__(self,other):
        return self.x >= other.x and self.y >= other.y