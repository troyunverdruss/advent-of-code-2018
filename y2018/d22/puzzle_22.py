from helpers.helpers import Point, read_raw_entries
import networkx as nx


class RegionNode:
    def __init__(self, region, loc, tool):
        self.region = region
        self.loc = loc
        self.tool = tool

    def __repr__(self):
        return repr('({}, {}), {}'.format(self.loc.x, self.loc.y, self.tool))


class Region:
    _allowed_tools = {
        0: ['C', 'T'],  # Rocky: climbing, torch
        1: ['C', 'N'],  # Wet: climbing, neither
        2: ['T', 'N'],  # Narrow: torch, neither
    }

    def __init__(self, loc, target, cave, depth):
        self.loc = loc
        self.target = target
        self.cave = cave
        self.depth = depth

        self._geo_index = None
        self._erosion_level = None
        self._type = None

        self.type()

        self.nodes = {
            self.allowed_tools()[0]: RegionNode(self, self.loc, self.allowed_tools()[0]),
            self.allowed_tools()[1]: RegionNode(self, self.loc, self.allowed_tools()[1]),
        }

    def geo_index(self):
        if self._geo_index is not None:
            return self._geo_index

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

        self._erosion_level = (self.geo_index() + self.depth) % 20183
        return self._erosion_level

    def type(self):
        if self._type is not None:
            return self._type

        self._type = self.erosion_level() % 3
        # print('Computed type for {}: {}'.format(self.loc, self._type))

        return self._type

    def allowed_tools(self):
        return Region._allowed_tools[self.type()]


def solve_22_part_1(depth, target):
    cave = {}
    risk = 0
    for x in range(0, target.x + 1):
        for y in range(0, target.y + 1):
            region = Region(Point(x, y), target, cave, depth)
            cave[Point(x, y)] = region

            risk += region.type()

    return risk


def solve_22_part_2(depth, target):
    cave = {}
    for x in range(0, target.x + 50):
        for y in range(0, target.y + 50):
            region = Region(Point(x, y), target, cave, depth)
            cave[Point(x, y)] = region

    g = nx.Graph()

    for k, region in cave.items():
        allowed_tools = region.allowed_tools()
        g.add_edge(region.nodes[allowed_tools[0]], region.nodes[allowed_tools[1]], weight=7)

        for direction in [Point(-1, 0), Point(0, -1)]:
            if (region.loc.x == 0 and direction.x == -1) or (region.loc.y == 0 and direction.y == -1):
                continue

            neighbor = cave[region.loc + direction]
            for tool in allowed_tools:
                if tool in neighbor.allowed_tools():
                    g.add_edge(region.nodes[tool], neighbor.nodes[tool], weight=1)

    path_length = nx.dijkstra_path_length(g, source=cave[Point(0, 0)].nodes['T'], target=cave[target].nodes['T'])
    return path_length


if __name__ == '__main__':
    entries = read_raw_entries(__file__, 'input.txt')
    depth = int(entries[0].split()[1])
    x, y = entries[1].split()[1].split(',')
    target = Point(int(x), int(y))
    risk = solve_22_part_1(depth, target)
    print('Risk: {}'.format(risk))

    time = solve_22_part_2(depth, target)
    print('Total distance in minutes: {}'.format(time))
