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


class Point3d:
    def __init__(self, x=None, y=None, z=None, id=''):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __add__(self, other):
        # Changing this will probably break some of the older puzzles, but
        # I think it's better this way ...
        return Point3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        if type(other) != Point3d:
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return repr('{}({},{},{})'.format(self.id, self.x, self.y, self.z))

    def __hash__(self):
        return hash('{}({},{},{})'.format(self.id, self.x, self.y, self.z))

    def __str__(self):
        return '{}({},{},{})'.format(self.id, self.x, self.y, self.z)


def get_min_max(points: List[Point]):
    min_x = min(points, key=lambda s: s.x).x
    max_x = max(points, key=lambda s: s.x).x
    min_y = min(points, key=lambda s: s.y).y
    max_y = max(points, key=lambda s: s.y).y
    return min_x, max_x, min_y, max_y


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def manhattan_distance_3d(a: Point3d, b: Point3d) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)
