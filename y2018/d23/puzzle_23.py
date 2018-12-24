import re
from typing import List

from helpers.helpers import Point3d, read_raw_entries, manhattan_distance_3d


class Nanobot:
    def __init__(self, loc: Point3d, radius):
        self.loc = loc
        self.radius = int(radius)

    def __repr__(self):
        return repr('{},{}'.format(self.loc, self.radius))


def solve_23(nanobots: List[Nanobot]):
    nanobot_with_max_radius = max(nanobots, key=lambda n: n.radius)
    print('Nanobot with max radius: {}'.format(nanobot_with_max_radius))

    in_range = 0
    for n in nanobots:
        if manhattan_distance_3d(nanobot_with_max_radius.loc, n.loc) <= nanobot_with_max_radius.radius:
            in_range += 1

    return in_range


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
