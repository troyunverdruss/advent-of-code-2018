from collections import deque
from copy import deepcopy

from helpers.helpers import get_min_max, Point
from days.day17.puzzle_17 import parse_real_input, print_state


def solve_17(points, still=False):
    min_x, max_x, min_y, max_y = get_min_max(points)
    print(min_x, max_x, min_y, max_y)

    clay = {}
    water = {}
    for point in points:
        clay[point] = '#'

    drop_points = deque([Point(500, 0)])
    already_dropped_from = {}

    down = Point(0, 1)
    left = Point(-1, 0)
    right = Point(1, 0)
    up = Point(0, -1)

    while len(drop_points) > 0:
        # print_state(clay, water, min_x, max_x, min_y, max_y)

        drop_point = drop_points.popleft()
        if drop_point in already_dropped_from:
            continue

        already_dropped_from[drop_point] = True

        loc = deepcopy(drop_point)

        keep_filling = True
        filling = False
        while keep_filling:
            # print_state(clay, water, min_x, max_x, min_y, max_y)

            if loc + down in clay or filling:
                filling = True
                water[loc] = '~'
                currently_filling = deque([loc])

                test = loc + left
                while test not in clay:
                    water[test] = '~'
                    currently_filling.append(test)
                    if test + down not in clay and (test + down not in water or water[test + down] == '|'):
                        drop_points.append(test)
                        keep_filling = False
                        filling = False
                        break
                    else:
                        test = test + left

                # go right
                test = loc + right
                while test not in clay:
                    water[test] = '~'
                    currently_filling.append(test)
                    if test + down not in clay and (test + down not in water or water[test + down] == '|'):
                        drop_points.append(test)
                        keep_filling = False
                        filling = False
                        break
                    else:
                        test = test + right

                loc = loc + up
                if not keep_filling:
                    for w in currently_filling:
                        water[w] = '|'
            else:
                water[loc] = '|'
                loc += down
                if loc.y > max_y:
                    break

    print('water len: {}'.format(len(water)))
    water_count = 0
    still_water = 0
    for w in water:
        if min_y <= w.y <= max_y:
            water_count += 1
            if water[w] == '~':
                still_water += 1

    # for y in range(min_y, max_y + 1):
    #     for x in range(min_x-50, max_x + 50):
    #         if Point(x, y) in water:
    #             water_count += 1


    # print_state(clay, water, min_x, max_x, min_y, max_y)

    if still:
        return still_water
    else:
        return water_count

if __name__ == '__main__':
    points = parse_real_input('input.txt')
    r = solve_17(points)
    print('Water squares: {}'.format(r))

    points = parse_real_input('input.txt')
    r = solve_17(points, still=True)
    print('Still water squares: {}'.format(r))

    # 37530, 38472, 38451