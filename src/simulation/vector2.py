class Vector2:

    def __init__(self, *args):
        self.x : int = -1
        self.y : int = -1
        self.set(*args)

    #args is either Vector2 or 2 ints
    def set(self, *args):
        if len(args) == 2:
            x, y = args

            if not(isinstance(x,int) and isinstance(y,int)):
                return NotImplemented

            self.x = args[0]
            self.y = args[1]
        else:
            args = args[0]

            if len(args) < 2:
                return NotImplemented

            if isinstance(args, tuple) or \
                isinstance(args, list) or \
                isinstance(args, Vector2):

                self.set(args[0],args[1])
            else:
                return NotImplemented

    def distance(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return max(abs(self.x-other.x), abs(self.y-other.y))

    def __getitem__(self, item):
        match item:
            case 0: return self.x
            case 1: return self.y
            case _: return NotImplemented

    def __iter__(self):
        return iter([self.x, self.y])

    def __len__(self):
        return 2

    def __add__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return Vector2(self.x+other.x, self.y+other.y)

    def __hash__(self):
        return hash((self.x,self.y))

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
