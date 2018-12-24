from typing import List


def read_numeric_entries(input):
    entries = []
    with open(input, 'r', encoding='utf8') as f:
        for line in f:
            entries.append(int(line.strip()))

    return entries


def read_raw_entries(input, strip=True):
    entries = []
    with open(input, 'r', encoding='utf8') as f:
        for line in f:
            if strip:
                entries.append(line.strip())
            else:
                entries.append(line)

    return entries


class Point:
    def __init__(self, x=None, y=None, id=''):
        self.id = id
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        # Changing this will probably break some of the older puzzles, but
        # I think it's better this way ...
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if type(other) != Point:
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return repr('{}({},{})'.format(self.id, self.x, self.y))

    def __hash__(self):
        return hash('{}({},{})'.format(self.id, self.x, self.y))

    def __str__(self):
        return '{}({},{})'.format(self.id, self.x, self.y)

    @staticmethod
    def directions():
        return {'UP': Point(0, 1), 'DOWN': Point(0, -1), 'LEFT': Point(-1, 0), 'RIGHT': Point(1, 0)}


def get_min_max(points: List[Point]):
    min_x = min(points, key=lambda s: s.x).x
    max_x = max(points, key=lambda s: s.x).x
    min_y = min(points, key=lambda s: s.y).y
    max_y = max(points, key=lambda s: s.y).y
    return min_x, max_x, min_y, max_y


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)
