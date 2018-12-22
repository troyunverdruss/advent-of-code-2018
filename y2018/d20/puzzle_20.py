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
        return repr('{} {}'.format(self.origin, self.index))


def solve_20(route_str):
    route = list(route_str)

    true_origin = Point(0, 0)
    dirs = {
        'N': Point(0, 1),
        'S': Point(0, -1),
        'W': Point(-1, 0),
        'E': Point(1, 0)
    }

    to_walk = deque([StartPoint(0, true_origin, 0)])

    g = nx.Graph()
    g.add_node(true_origin)

    while to_walk:
        start_point = to_walk.popleft()

        index = start_point.index
        last_loc = deepcopy(start_point.origin)
        depth = start_point.depth

        while True:
            value = route[index]

            if value == '^':
                pass
            elif value in ['N', 'S', 'W', 'E']:
                new_loc = last_loc + dirs[value]
                g.add_node(new_loc)
                g.add_edge(last_loc, new_loc)
                last_loc = new_loc
            elif value == '(':
                depth += 1
                process_inner_paren(last_loc, index, route, to_walk, depth)
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
            elif value == '$':
                break

            index += 1

    max_distance = 0
    for node in g.nodes:
        distance = nx.shortest_path_length(g, source=true_origin, target=node)
        if distance > max_distance:
            max_distance = distance

    nx.write_gml(g, 'graph.gml', str)
    return max_distance


def process_inner_paren(last_loc, index, route, to_walk, depth):
    p = StartPoint(index + 1, Point(last_loc.x, last_loc.y), depth)
    to_walk.append(p)
    while True:
        index += 1
        v = route[index]
        if v == '|':
            p = StartPoint(index + 1, Point(last_loc.x, last_loc.y), depth)
            to_walk.append(p)
        elif v == ')':
            if depth > 0:
                depth -= 1
            else:
                break
        elif v == '(':
            depth += 1
            process_inner_paren(last_loc, index, route, to_walk, depth)
        elif v == '$':
            break


if __name__ == '__main__':
    input = read_raw_entries('input.txt')
    r = solve_20(input[0].strip())
    print('Max distance: {}'.format(r))
