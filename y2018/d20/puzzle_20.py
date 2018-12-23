from collections import deque
from copy import deepcopy

import networkx as nx

from helpers.helpers import read_raw_entries, Point


class StartPoint:
    def __init__(self, index, origin, depth):
        self.index = index
        self.origin = origin
        self.depth = depth

    def __repr__(self):
        return repr('{} {} {}'.format(self.origin, self.index, self.depth))

    def __eq__(self, other):
        return self.index == other.index and self.origin == other.origin and self.depth == other.depth

    def __hash__(self):
        return hash('{} {} {}'.format(self.index, self.origin, self.depth))


def solve_20(route_str):
    route = list(route_str)

    true_origin = Point(0, 0)
    dirs = {
        'N': Point(0, 1),
        'S': Point(0, -1),
        'W': Point(-1, 0),
        'E': Point(1, 0)
    }

    to_walk = {StartPoint(0, true_origin, 0)}
    seen = set()

    g = nx.DiGraph()
    g.add_node(true_origin)

    print('Route length: {}'.format(len(route)))

    skip_count = 0
    while to_walk:
        # print(to_walk)
        start_point = to_walk.pop()

        if start_point in seen:
            skip_count += 1
            continue
        seen.add(start_point)

        index = start_point.index
        last_loc = deepcopy(start_point.origin)
        depth = start_point.depth

        # print('Starting at start point: {}'.format(start_point))
        while True:
            value = route[index]

            if value == '^':
                pass
            elif value in ['N', 'S', 'W', 'E']:
                new_loc = last_loc + dirs[value]
                # g.add_node(new_loc)
                g.add_edge(last_loc, new_loc)
                last_loc = new_loc
            elif value == '(':
                process_inner_paren(last_loc, index, route, to_walk, depth + 1)
                break

            elif value == '|':
                index += 1
                start_depth = depth
                while True:
                    if route[index] == '(':
                        depth += 1
                    if route[index] == ')':
                        if depth > start_depth:
                            depth -= 1
                        else:
                            break
                    index += 1
            elif value == ')':
                depth -= 1
            elif value == '$':
                break

            index += 1

    nx.write_gml(g, 'graph.gml', str)

    all_simple_paths = nx.single_source_shortest_path(g, source=Point(0, 0))
    max_distance = 0
    for k in all_simple_paths.keys():
        if len(all_simple_paths[k]) > max_distance:
            max_distance = len(all_simple_paths[k])

    print('max: {}'.format(max_distance - 1))

    return max_distance - 1


def process_inner_paren(last_loc, index, route, to_walk, depth):
    p = StartPoint(index + 1, Point(last_loc.x, last_loc.y), depth)
    to_walk.add(p)
    start_depth = depth
    while True:
        index += 1
        v = route[index]
        if v == '|' and depth == start_depth:
            # if route[index + 1] == ')':
            #     p = StartPoint(index + 2, Point(last_loc.x, last_loc.y), depth - 1)
            # else:
            p = StartPoint(index + 1, Point(last_loc.x, last_loc.y), depth)
            if p not in to_walk:
                to_walk.add(p)
        elif v == ')':
            depth -= 1
            if depth < start_depth:
                break
        elif v == '(':
            depth += 1
            # process_inner_paren(last_loc, index, route, to_walk, depth + 1)
        elif v == '$':
            break


if __name__ == '__main__':
    input = read_raw_entries('input.txt')
    r = solve_20(input[0].strip())
    print('Max distance: {}'.format(r))
