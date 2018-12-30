from collections import deque
from typing import List
from itertools import combinations
import anytree

from helpers.helpers import Point4d, manhattan_distance_4d, read_raw_entries

id = 0


class Constellation:
    def __init__(self, init: Point4d):
        global id
        self.id = id
        id += 1

        self._min = Point4d(init.x, init.y, init.z, init.t)
        self._max = Point4d(init.x, init.y, init.z, init.t)
        self.points = {init}
        self._joined = []

    def can_join(self, point: Point4d) -> bool:
        for p in self.points:
            if manhattan_distance_4d(p, point) <= 3:
                # print('True {} {}'.format(p, point))
                return True
        return False

    def join(self, point):
        self.points.add(point)

    def join_c(self, constellation: 'Constellation'):
        self.points = self.points.union(constellation.points)
        self._joined.append(constellation.id)

    def can_join_c(self, constellation: 'Constellation') -> bool:
        for p in constellation.points:
            if self.can_join(p):
                return True
        return False

def parse_input(input):
    entries = read_raw_entries(input)
    points = []
    for entry in entries:
        c = entry.split(',')

        if len(c) != 4:
            continue

        points.append(Point4d(c[0], c[1], c[2], c[3]))
    return points


def build_join_list(to_join: List):
    nodes = {}
    parents = []

    for pair in to_join:
        if pair[0] in nodes.keys():
            n1 = nodes[pair[0]]
        else:
            n1 = anytree.Node(pair[0])
            n1.constellation = pair[0]
            nodes[pair[0]] = n1
            parents.append(n1)

        if pair[1] in nodes.keys():
            n2 = nodes[pair[1]]
        else:
            n2 = anytree.Node(pair[1])
            n2.constellation = pair[1]
            nodes[pair[1]] = n2

        n2.parent = n1

    return parents


def solve_25(points: List[Point4d]):
    total_points = len(points)
    constellations = deque([Constellation(points[0])])

    # First let's stuff the points into constellations
    for p in points[1:]:
        joined = False
        for c in constellations:
            if c.can_join(p):
                c.join(p)
                joined = True
                break
        if not joined:
            constellations.append(Constellation(p))

    # print_current_point_status(constellations, total_points)

    # Now let's see if we can join any constellations together
    last_len = len(constellations)
    print('Initial length: {}'.format(last_len))
    no_change_count = 0
    while True:
        compact_constellations(constellations, total_points)
        if len(constellations) == last_len:
            no_change_count += 1
        else:
            no_change_count = 0
            print('New length: {}'.format(len(constellations)))

        last_len = len(constellations)
        print_current_point_status(constellations, total_points)

        if no_change_count > 5:
            break

    return len(constellations)


def print_current_point_status(constellations, total_points):
    current_points = set()
    for c in constellations:
        for p in c.points:
            current_points.add(p)
    print('Point count: {}, Expected: {}'.format(len(current_points), total_points))


def compact_constellations(constellations, total_points):
    to_join = []

    combos = list(combinations(constellations, r=2))

    for pair in combos:
        if pair[0].can_join_c(pair[1]):
            to_join.append(pair)

    # print_current_point_status(constellations, total_points)

    parent_list = build_join_list(to_join)

    for parent in parent_list:
        descendants = parent.descendants
        for d in descendants:
            parent.constellation.join_c(d.constellation)
            constellations.remove(d.constellation)

    # print_current_point_status(constellations, total_points)


if __name__ == '__main__':
    points = parse_input('input.txt')
    c = solve_25(points)
    print(c)
