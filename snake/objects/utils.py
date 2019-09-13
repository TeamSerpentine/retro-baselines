

class Point:
    """
        Helper function to maintain x, y position on the board.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        # Required for set comparisons
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"(x={self.x}, y={self.y})"

    def __repr__(self):
        return self.__str__()

    def clone(self):
        return Point(self.x, self.y)

    def as_value(self):
        return self.x, self.y
