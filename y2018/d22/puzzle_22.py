from helpers.helpers import Point, read_raw_entries


class Region:
    def __init__(self, loc, target, cave, depth):
        self.loc = loc
        self.target = target
        self.cave = cave
        self.depth = depth

        self._geo_index = None
        self._erosion_level = None
        self._type = None

        self._building = True
        self.type()
        self._building = False

    def geo_index(self):
        if self._geo_index is not None:
            return self._geo_index

        if not self._building:
            print('Cache miss for {} (geo_index)'.format(self.loc))
        if self.loc == Point(0, 0):
            self._geo_index = 0
        elif self.loc == self.target:
            self._geo_index = 0
        elif self.loc.y == 0:
            self._geo_index = self.loc.x * 16807
        elif self.loc.x == 0:
            self._geo_index = self.loc.y * 48271
        else:
            x_minus_one = self.cave[Point(self.loc.x - 1, self.loc.y)].erosion_level()
            y_minus_one = self.cave[Point(self.loc.x, self.loc.y - 1)].erosion_level()
            self._geo_index = x_minus_one * y_minus_one

        return self._geo_index

    def erosion_level(self):
        if self._erosion_level is not None:
            return self._erosion_level

        if not self._building:
            print('Cache miss for {} (erosion_level)'.format(self.loc))
        self._erosion_level = (self.geo_index() + self.depth) % 20183
        return self._erosion_level

    def type(self):
        if self._type is not None:
            return self._type

        if not self._building:
            print('Cache miss for {} (type)'.format(self.loc))
        self._type = self.erosion_level() % 3
        # print('Computed type for {}: {}'.format(self.loc, self._type))

        return self._type

    def display_type(self):
        if self.type() == 0:
            # Rocky
            self._type = '.'
        elif self.type() == 1:
            # Wet
            self._type = '='
        elif self.type() == 2:
            # Narrow
            self._type = '|'
        else:
            Exception('Unknown type: {}'.format(self.type()))


def solve_22(depth, target):
    cave = {}
    risk = 0
    for x in range(0, target.x + 1):
        for y in range(0, target.y + 1):
            region = Region(Point(x, y), target, cave, depth)
            cave[Point(x, y)] = region

            risk += region.type()

    return risk


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    depth = int(entries[0].split()[1])
    x, y = entries[1].split()[1].split(',')
    target = Point(int(x), int(y))
    risk = solve_22(depth, target)
    print('Risk: {}'.format(risk))
