from collections import Counter
from typing import Dict
from copy import deepcopy

from helpers.helpers import read_raw_entries, Point, get_min_max


def print_state(time_id, grid):
    print('Time: {}'.format(time_id))

    min_x, max_x, min_y, max_y = get_min_max(list(grid.keys()))
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            print(grid[Point(x, y)], end='')
        print('')
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


def solve_18(entries, max_minutes=10):
    grid = {}
    y = 0
    for entry in entries:
        x = 0
        for v in list(entry):
            grid[Point(x, y)] = v
            x += 1
        y += 1

    # print_state('Initial', grid)

    minutes = 0
    last_value = 0

    past_grids = {}

    multiples_under_1000 = [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64, 80, 100, 125, 128, 160, 200, 250, 256, 320, 400, 500, 512, 625, 640, 800]
    # for m in multiples_under_1000:
    #     past_grids[m] = []

    period = None
    while minutes < max_minutes:
        run_iteration(grid)
        minutes += 1

        # for m in multiples_under_1000:
        #     if minutes%m == 0:
        s = str(list(map(lambda v: grid[v], sorted(grid, key=lambda c: (c.x, c.y)))))
        # s = ''
        # for v in vals:
        #     s += str(grid[v])

        key = hash(s)

        if key in past_grids:
            period = minutes - past_grids[key]
            k = (1000000000 - past_grids[key]) % period
            print('part 2: {}'.format(past_grids[]))

        #     print('Min: {}, matches: {}'.format(minutes, past_grids[key]))
        #     past_grids[key].append(minutes)
                    # past_grids[key].append(minutes)
                # else:
                #     past_grids[key] = [minutes]

        else:
            past_grids[key] = minutes
            # past_grids.append(key)
        # for multis in multiples_under_1000:
        #     if minutes % multis == 0:
        #         key = hash(str(grid))
        #         if multis not in past_grids:
        #             past_grids[multis] = []
        #         value = compute_part_a(grid)
        #         past_grids[multis].append(value)
        #         c = Counter(past_grids[multis])
        #         v = list(sorted(c))[len(c)-3:]
        #         print('{} => {} {}'.format(multis,value, v))

        if minutes in list(range(465, 521)):
            # 28 difference
            print('{}: {}'.format(minutes, compute_part_a(grid)))


        # curr_value = compute_part_a(grid)

        # curr_multiple = 1000000000.0 / minutes
        # if curr_multiple in multiples_under_1000:
        #     past_grids[curr_multiple].append(curr_value)
        #     print('{}: {}'.format(curr_multiple, past_grids[curr_multiple]))

        # if curr_value not in past_grids:
        #     past_grids[curr_value] = [minutes]
        # else:
        #     print('Current value: {} (minute: {}) matched previous minutes: {}'.format(curr_value, minutes, past_grids[curr_value]))
        #     past_grids[curr_value].append(minutes)

        # past_grids[minutes] = curr_value
        # if curr_value in past
        # if minutes % 100 == 0:
        #     print_state(minutes, grid)
        #     lumberyards, wooded = get_lumberyards_wood(grid)
        #     print('After minute: {}'.format(minutes))
        #     curr_value = lumberyards * wooded
        #     print('Lumberyards: {}, wooded: {}, ratio: {}, resource value: {}, diff: {}, per year: {}'.format(lumberyards, wooded, lumberyards / wooded, curr_value, curr_value - last_value, curr_value / minutes))
        #     last_value = curr_value

    return compute_part_a(grid)

def get_lumberyards_wood(grid):
    lumberyards = 0
    wooded = 0

    for k in grid.keys():
        if grid[k] == '#':
            lumberyards += 1
        elif grid[k] == '|':
            wooded += 1
    return lumberyards, wooded


def compute_part_a(grid):
    lumberyards, wooded = get_lumberyards_wood(grid)
    return lumberyards * wooded


if __name__ == '__main__':
    entries = read_raw_entries(__file__, 'input.txt')
    r = solve_18(entries)
    print(r)

    entries = read_raw_entries(__file__, 'input.txt')
    r = solve_18(entries, 1000000000)
    print(r)
