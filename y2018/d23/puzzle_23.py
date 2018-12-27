import re
from typing import List, Tuple
from helpers.helpers import Point3d, read_raw_entries, manhattan_distance_3d

import z3


class Nanobot:
    def __init__(self, loc: Point3d, radius):
        self.loc = loc
        self.radius = int(radius)

    def __repr__(self):
        return repr('{},{}'.format(self.loc, self.radius))

    def loc_tuple(self):
        return (self.loc.x, self.loc.y, self.loc.z)


def solve_23(nanobots: List[Nanobot]):
    nanobot_with_max_radius = max(nanobots, key=lambda n: n.radius)
    print('Nanobot with max radius: {}'.format(nanobot_with_max_radius))

    in_range = 0
    for n in nanobots:
        if manhattan_distance_3d(nanobot_with_max_radius.loc, n.loc) <= nanobot_with_max_radius.radius:
            in_range += 1

    return in_range

def search_point(point: Point3d, bots: List[Nanobot]):
    found_bots = []
    for b in bots:
        if manhattan_distance_3d(point, b.loc) <= b.radius:
            found_bots.append(b)

    return found_bots

def z3abs(n):
    return z3.If(n >= 0, n, -n)


def z3distance(a: Tuple, b: Tuple):
    return z3abs(a[0] - b[0]) + \
           z3abs(a[1] - b[1]) + \
           z3abs(a[2] - b[2])


def solve_23_part_2(nanobots: List[Nanobot]):
    print('Starting up')
    origin = (0, 0, 0)
    x, y, z, in_range = z3.Ints('x y z in_range')

    in_range = in_range * 0
    print('Vars declared')

    for bot in nanobots:
        in_range += z3.If(z3distance(bot.loc_tuple(), (x, y, z)) <= bot.radius, 1, 0)

    print('In range calc prep done')
    optimizer = z3.Optimize()

    print('Created optimizer, setting max/min functions')
    optimizer.maximize(in_range)
    optimizer.minimize(z3distance(origin, (x, y, z)))

    print('Checking optimizer')
    optimizer.check()

    print('Getting model')
    model = optimizer.model()

    print('Returning values')
    origin_loc = Point3d(0, 0, 0)
    found_loc = Point3d(model[x].as_long(), model[y].as_long(), model[z].as_long())
    distance_to_found_loc = manhattan_distance_3d(origin_loc, found_loc)
    bots_at_loc = search_point(found_loc, nanobots)

    print('Distance from {} to {}: {}. Bots in range: {}'.format(origin_loc, found_loc, distance_to_found_loc, len(bots_at_loc)))
    return distance_to_found_loc


def parse_input(input):
    global nanobots
    entries = read_raw_entries(input)
    p = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
    nanobots = []
    for entry in entries:
        m = p.match(entry)
        nanobots.append(Nanobot(Point3d(m.group(1), m.group(2), m.group(3)), m.group(4)))

    return nanobots


if __name__ == '__main__':
    nanobots = parse_input('input.txt')

    in_range = solve_23(nanobots)
    print('Part 1, in range: {}'.format(in_range))

    distance = solve_23_part_2(nanobots)
    print('Distance to closest point: {}'.format(distance))

    # 87900620 too low
    # 88353407 too low
    # 100985898 ?
