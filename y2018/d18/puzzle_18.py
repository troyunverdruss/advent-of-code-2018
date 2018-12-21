from collections import Counter
from typing import Dict

from helpers.helpers import read_raw_entries, Point, get_min_max


def print_state(grid):
    min_x, max_x, min_y, max_y = get_min_max(list(grid.keys()))
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            print(grid[Point(x, y)], end='')
        print('')
    print('')


NEIGHBORS = [
    Point(-1, -1), Point(0, -1), Point(1, -1),
    Point(-1, 0), Point(1, 0),
    Point(-1, 1), Point(0, 1), Point(1, 1)
]


def get_neighbor_values(loc: Point, grid: Dict):
    neighbor_values = []
    for neighbor in NEIGHBORS:
        if loc + neighbor in grid:
            neighbor_values.append(grid[loc + neighbor])
    return neighbor_values


def run_iteration(grid):
    new_values = {}

    for loc in grid.keys():
        neighbor_values = get_neighbor_values(loc, grid)
        counter = Counter(neighbor_values)
        if grid[loc] == '.' and counter['|'] >= 3:
            new_values[loc] = '|'
        elif grid[loc] == '|' and counter['#'] >= 3:
            new_values[loc] = '#'
        elif grid[loc] == '#':
            if not (counter['|'] >= 1 and counter['#']):
                new_values[loc] = '.'

    for pos in new_values.keys():
        grid[pos] = new_values[pos]


def solve_18(entries):
    grid = {}
    y = 0
    for entry in entries:
        x = 0
        for v in list(entry):
            grid[Point(x, y)] = v
            x += 1
        y += 1

    print_state(grid)

    minutes = 0
    while minutes < 10:
        run_iteration(grid)
        minutes += 1

    return compute_part_a(grid)


def compute_part_a(grid):
    lumberyards = 0
    wooded = 0

    for k in grid.keys():
        if grid[k] == '#':
            lumberyards += 1
        elif grid[k] == '|':
            wooded += 1

    return lumberyards * wooded


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    r = solve_18(entries)
    print(r)
