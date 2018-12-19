from helpers.helpers import read_raw_entries, Point, get_min_max
from collections import deque
import re
from copy import deepcopy


def parse_input(input):
    entries = read_raw_entries(input)
    points = []
    for entry in entries:
        parts = entry.split()

        if 'x' in parts[0]:
            x = parts[0].split('=')[1].replace(',', '')

            s, e = parts[1].split('=')[1].split('..')
            for y in range(int(s), int(e) + 1):
                p = Point(x, y)
                points.append(p)
        else:
            y = parts[0].split('=')[1].replace(',', '')

            s, e = parts[1].split('=')[1].split('..')
            for x in range(int(s), int(e) + 1):
                p = Point(x, y)
                points.append(p)

    return points


def print_state(clay, water, min_x, max_x, min_y, max_y):
    for x in range(min_x, max_x + 1):
        if x == 500:
            print('x', end='')
        else:
            print('.', end='')
    print('')

    for y in range(min_y,  max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) in clay:
                print(clay[Point(x,y)], end='')
            elif Point(x, y) in water:
                print(water[Point(x, y)], end='')
            else:
                print('.', end='')
        print('')
    print('')


def solve_17(input):
    points = parse_input(input)
    min_x, max_x, min_y, max_y = get_min_max(points)
    print(min_x, max_x, min_y, max_y)

    clay = {}
    water = {}
    for point in points:
        clay[point] = '#'

    drop_points = deque([Point(500, 0)])

    # go down from first drop point
    down = Point(0, 1)
    left = Point(-1, 0)
    right = Point(1, 0)
    up = Point(0, -1)
    tick = 0
    while len(drop_points) > 0:
        tick += 1

        drop_point = drop_points.popleft()
        loc = deepcopy(drop_point)
        print('Dropping from {}'.format(drop_point))


        keep_filling = True
        while keep_filling:

            # print_state(clay, water, min_x, max_x, min_y, max_y)
            if loc + down in clay or (loc + down in water and water[loc + down] == '~'):
                water[loc] = '~'

                # go left
                test = loc + left
                while test not in clay:
                    water[test] = '~'
                    if test + down not in clay and test + down not in water:
                        drop_points.append(test)
                        # if drop_point in drop_points:
                        #     drop_points.remove(drop_point)
                        # drop_points.append(drop_point)
                        break
                    else:
                        test = test + left

                # go right
                test = loc + right
                while test not in clay:
                    water[test] = '~'
                    if test + down not in clay and test + down not in water:
                        drop_points.append(test)
                        # if drop_point in drop_points:
                        #     drop_points.remove(drop_point)
                        # drop_points.append(drop_point)
                        keep_filling = False
                        break
                    else:
                        test = test + right

                loc = loc + up
                if loc.y < drop_point.y:
                    break

            else:
                loc = loc + down
                if loc.y > max_y:
                    break
                elif loc.y >= min_y:
                    water[loc] = '|'

            print_state(clay, water, min_x, max_x, min_y, max_y)


    print_state(clay, water, min_x, max_x, min_y, max_y)

    return len(water)




if __name__ == '__main__':
    r = solve_17('input.txt')
    print('Water squares: {}'.format(r))
