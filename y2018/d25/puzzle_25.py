from typing import List

from helpers.helpers import Point4d, manhattan_distance_4d, read_raw_entries


def parse_input(input):
    entries = read_raw_entries(input)
    points = []
    for entry in entries:
        c = entry.split(',')

        if len(c) != 4:
            continue

        points.append(Point4d(c[0], c[1], c[2], c[3]))
    return points


def solve_25(points: List[Point4d]):
    pass
