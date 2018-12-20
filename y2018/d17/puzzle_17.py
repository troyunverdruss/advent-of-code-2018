from helpers.helpers import read_raw_entries, Point, get_min_max
from collections import deque
import re
from copy import deepcopy
from anytree import Node, RenderTree, search as at_search




def parse_real_input(input):
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
    f = open("test_out.txt", "w")

    for x in range(min_x-1, max_x + 2):
        if x == 500:
            print('x', end='')
            f.write('x\n')
        else:
            print('.', end='')
            f.write('.')
    print('')
    f.write('\n')

    for y in range(min_y-1, max_y + 2):
        for x in range(min_x-1, max_x + 2):
            if Point(x, y) in clay:
                print(clay[Point(x, y)], end='')
                f.write(clay[Point(x, y)])
            elif Point(x, y) in water:
                print(water[Point(x, y)], end='')
                f.write(water[Point(x, y)])
            else:
                print('.', end='')
                f.write('.')
        print('')
        f.write('\n')
    print('')
    f.write('\n')
    f.close()


def solve_17(points):

    min_x, max_x, min_y, max_y = get_min_max(points)
    print(min_x, max_x, min_y, max_y)

    clay = {}
    water = {}
    for point in points:
        clay[point] = '#'

    # drop_points = deque([Point(500, 0)])
    water_origin = Node(Point(500, 0), loc=Point(500, 0), run=False, origin=True)
    drop_point: Node = water_origin

    # drop_point_parents = {}

    # go down from first drop point
    down = Point(0, 1)
    left = Point(-1, 0)
    right = Point(1, 0)
    up = Point(0, -1)
    tick = 0
    lowest_drop_point = -1
    previous_drop_points = []
    while drop_point:
        print(previous_drop_points)
        drop_point = \
                at_search.findall(water_origin, filter_=lambda n: n.is_leaf and n.depth == water_origin.height)[0]
        if drop_point.run:
            break

        drop_point.run = True
        previous_drop_points.append(drop_point.loc)
        tick += 1

        # drop_point = drop_points.popleft()

        loc = deepcopy(drop_point.loc)
        # print('Dropping from {}'.format(drop_point))

        # if loc.y > lowest_drop_point:
        #     print('Dropping for new depth: {}'.format(loc.y))
        #     lowest_drop_point = loc.y
            # print_state(clay, water, min_x, max_x, min_y, max_y)

        keep_filling = True
        while keep_filling:

            # print_state(clay, water, min_x, max_x, min_y, max_y)
            if loc + down in clay or (loc + down in water and water[loc + down] == '~'):
                if loc + down in water and water[loc + down] == '~':
                    quick_test = loc + down
                    contained_left = True
                    contained_right = True
                    previous_drop_left = False
                    previous_drop_right = False
                    on_clay = False

                    if quick_test in clay:
                        on_clay = True

                    while quick_test.x >= min_x or quick_test in clay:
                        if quick_test in previous_drop_points:
                            previous_drop_left = True

                        if (quick_test not in water or water[quick_test] != '~') and quick_test not in clay:
                            contained_left = False
                            break

                        quick_test += left

                    quick_test = loc + down
                    while quick_test.x <= max_x or quick_test in clay:
                        if quick_test in previous_drop_points:
                            previous_drop_right = True
                        if (quick_test not in water or water[quick_test] != '~') and quick_test not in clay:
                            contained_right = False
                            break

                        quick_test += right

                    if (contained_left or contained_right) or (not contained_left and not previous_drop_left) or (not contained_right and not previous_drop_right):
                        pass
                    else:
                        drop_point.parent = None
                        break

                water[loc] = '~'

                # go left
                test = loc + left
                while test not in clay:
                    # if len(drop_points) > 0:
                    #     if test.y < min(drop_points, key=lambda p: p.y).y:
                    #         keep_filling = False
                    #         break

                    water[test] = '~'
                    if test + down not in clay and test + down not in water:
                        n = Node(test, parent=drop_point, loc=test, run=False)
                        if loc.y == drop_point.loc.y:
                            n.parent = drop_point.parent
                        keep_filling = False
                        break
                    else:
                        test = test + left

                # go right
                test = loc + right
                while test not in clay:
                    # if len(drop_points) > 0:
                    #     if test.y < min(drop_points, key=lambda p: p.y).y:
                    #         keep_filling = False
                    #         break
                    water[test] = '~'
                    if test + down not in clay and test + down not in water:
                        n = Node(test, parent=drop_point, loc=test, run=False)
                        if loc.y == drop_point.loc.y:
                            n.parent = drop_point.parent
                        keep_filling = False
                        break
                    else:
                        test = test + right

                loc = loc + up
                if loc.y < drop_point.loc.y:
                    drop_point.parent.run = False
                    drop_point.parent = None
                    # if drop_point.siblings:
                    #     # old = drop_point
                    #     # drop_point = drop_point.siblings[0]
                    #     # old.parent = None
                    #     drop_point.parent = None
                    # else:
                    #     while not drop_point.siblings:
                    #         # old = drop_point
                    #         # drop_point = drop_point.parent
                    #         # old.parent = None

                    # drop_point = \
                    #     at_search.findall(water_origin, filter_=lambda
                    #         n: n.is_leaf and n.depth == water_origin.height and n.hits == 0)[0]
                    # drop_point.hits += 1

                    # if drop_point in drop_point_parents:
                    #     parent_drop_point = drop_point_parents[drop_point]
                    #     move_or_append(water_origin, parent_drop_point)
                    #     del parent_drop_point
                    break


            else:
                loc = loc + down
                if loc.y > max_y:
                    if len(drop_point.siblings) > 0:
                        drop_point.parent = None
                    else:
                        old = drop_point
                        drop_point = old.parent
                        old.parent = None
                        while drop_point and len(drop_point.siblings) == 0:
                            old = drop_point
                            drop_point = old.parent
                            old.parent = None

                        else:
                            if drop_point:
                                old = drop_point
                                drop_point = old.parent
                                old.parent = None

                        if drop_point and not drop_point.parent and len(drop_point.children) == 0:
                            drop_point = None
                    break
                else:
                    water[loc] = '|'

            # print(drop_points)
            # print_state(clay, water, min_x, max_x, min_y, max_y)
            bla = 0

    print_state(clay, water, min_x, max_x, min_y, max_y)

    water_count = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) in water:
                water_count += 1

    return water_count


def move_or_append(deq: deque, item):
    if item in deq:
        deq.remove(item)
    deq.append(item)


if __name__ == '__main__':
    points = parse_real_input('input.txt')
    r = solve_17(points)
    print('Water squares: {}'.format(r))
