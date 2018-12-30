import uuid
from collections import deque
from copy import deepcopy
from typing import List, Tuple
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
            # else:
            #     print('False {} {}'.format(p, point))
        return False
        # if self._min.x - 3 <= point.x <= self._max.x + 3 \
        #         or self._min.y - 3 <= point.y <= self._max.y + 3 \
        #         or self._min.z - 3 <= point.z <= self._max.z + 3 \
        #         or self._min.t - 3 <= point.t <= self._max.t + 3:
        #     return True
        # return False

    def join(self, point):
        self.points.add(point)
        # self.recacl_min_max(point)

    def join_c(self, constellation: 'Constellation'):
        my_points = len(self.points)
        other_points = len(constellation.points)

        # a = deepcopy(self.points)
        # b = deepcopy(constellation.points)
        #
        self.points = self.points.union(constellation.points)
        self._joined.append(constellation.id)

        # if len(self.points) != my_points + other_points:
        #
        #     print('Joined {} + {} = {}, expected {}'.format(my_points, other_points, len(self.points), my_points + other_points))

        # self.recacl_min_max(constellation._min)
        # self.recacl_min_max(constellation._max)

    def can_join_c(self, constellation: 'Constellation') -> bool:
        for p in constellation.points:
            if self.can_join(p):
                return True
        return False
        # if self.can_join(constellation._min) or self.can_join(constellation._max):
        #     return True
        # return False

    # def recacl_min_max(self, point: Point4d):
    #     self._min.x = min(self._min.x, point.x)
    #     self._max.x = min(self._max.x, point.x)
    #     self._min.y = min(self._min.y, point.y)
    #     self._max.y = min(self._max.y, point.y)
    #     self._min.z = min(self._min.z, point.z)
    #     self._max.z = min(self._max.z, point.z)
    #     self._min.t = min(self._min.t, point.t)
    #     self._max.t = min(self._max.t, point.t)


def parse_input(input):
    entries = read_raw_entries(input)
    points = []
    for entry in entries:
        c = entry.split(',')

        if len(c) != 4:
            continue

        points.append(Point4d(c[0], c[1], c[2], c[3]))
    return points


def build_join_list(to_join: List, join_map=None, destroy=None):
    uniq_ids = []
    for c in to_join:
        for _ in c:
            if _ not in uniq_ids:
                uniq_ids.append(_)

    if len(to_join) == 0:
        return {}, None
    print('> Join list: {}'.format(len(uniq_ids)))

    if join_map is None:
        join_map = {to_join[0][0]: [to_join[0][1]]}
    if destroy is None:
        destroy = []

    for pair in to_join[1:]:
        if pair[0] in join_map.keys():
            join_map[pair[0]].append(pair[1])
        elif pair[0] in join_map.values():
            kvs = list(filter(lambda k, v: pair[0] in v, join_map.items()))
            assert len(kvs) == 1
            join_map[kvs[0]].append(pair[1])
        else:
            join_map[pair[0]] = [pair[1]]

    uniq_ids = []
    for k, v in join_map.items():
        if k not in uniq_ids:
            uniq_ids.append(k)
        for _ in v:
            if _ not in uniq_ids:
                uniq_ids.append(_)

    print('> Join map length: {}'.format(len(uniq_ids)))

    return join_map, destroy


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

    print_current_point_status(constellations, total_points)

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

    # for c in constellations:
    #     print('{}: {}'.format(c.id, c._joined))

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
    # print('Combos:')
    for c in combos:
        pass
        # print('{}, {}'.format(c[0].id, c[1].id))

    for pair in combos:
        if pair[0].can_join_c(pair[1]):
            to_join.append(pair)

    print_current_point_status(constellations, total_points)

    join_map, destroy = build_join_list(to_join)

    for k in join_map.keys():
        for c in join_map[k]:
            k.join_c(c)
            if c in constellations:
                constellations.remove(c)


if __name__ == '__main__':
    points = parse_input('input.txt')
    c = solve_25(points)
    print(c)

    # too high 355
    # too high 321
