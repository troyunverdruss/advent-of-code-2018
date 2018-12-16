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
    def __init__(self, x=None, y=None, id=None):
        self.id = id
        self.x = x
        self.y = y

    def __add__(self, other):
        # Changing this will probably break some of the older puzzles, but
        # I think it's better this way ...
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return repr('{}: ({},{})'.format(self.id, self.x, self.y))



def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)