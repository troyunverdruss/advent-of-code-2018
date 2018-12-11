from helpers.helpers import manhattan_distance, Point
import math
from collections import deque


def traverse_grid(origin, side_length, target_max):
    if target_max == 1:
        return origin

    grid = []
    for x in range(0, side_length):
        grid.append([])
        for y in range(0, side_length):
            grid[x].append(0)

    d = deque([
        Point(x=1, y=0),
        Point(x=0, y=-1),
        Point(x=-1, y=0),
        Point(x=0, y=1)
    ])

    cell = Point(x=origin.x, y=origin.y)
    grid[cell.x][cell.y] = 1

    cell += d[0]
    grid[cell.x][cell.y] = 1

    d.rotate(-1)

    i = 3
    temp_side_limit = 1
    inc_toggle = True

    while i <= target_max:

        for l in range(0, temp_side_limit):
            cell += d[0]

            if i == target_max:
                return cell

            value = compute_value(cell, grid)
            grid[cell.x][cell.y] = value

            if value > target_max:
                print('Found larger than target value: {}'.format(value))
                exit()


            i += 1

        if inc_toggle:
            temp_side_limit += 1
            inc_toggle = False
        else:
            inc_toggle = True

        d.rotate(-1)


def compute_value(cell, grid):
    value = 0
    dirs = [
        Point(-1, -1),
        Point(0, -1),
        Point(1, -1),
        Point(-1, 0),
        Point(1, 0),
        Point(-1, 1),
        Point(0, 1),
        Point(1, 1)
    ]

    for dir in dirs:
        value += grid[cell.x + dir.x][cell.y + dir.y]

    return value

def solve_3a(input):
    side_length = math.ceil(math.sqrt(input))
    if side_length % 2 == 0:
        side_length += 3

    center_index = math.floor(side_length / 2.0)
    origin = Point(x=center_index, y=center_index, id=1)

    target = traverse_grid(origin, side_length, input)

    return manhattan_distance(origin, target)


if __name__ == '__main__':
    r = solve_3a(289326)
    print(r)

    # r = solve_2b(entries)
    # print(r)
