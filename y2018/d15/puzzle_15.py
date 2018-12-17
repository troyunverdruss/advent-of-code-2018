from helpers.helpers import read_raw_entries, Point, manhattan_distance
from copy import deepcopy
import sys
from collections import deque
import itertools
from typing import List, Dict
from anytree import Node, RenderTree, search as anytree_search

ROUND = 0
FIGHTER = None


def find_closest_target(coords, target, elements):
    previous_move = {}
    distance = {}

    to_visit = deque()
    for d in directions:
        coords_ = (coords + d)
        to_visit.append(coords_)
        previous_move[coords_] = coords
        distance[coords_] = 1

    closest = None
    while len(to_visit) > 0:

        new_coords = to_visit.popleft()

        # if new_coords.x >= 0 and new_coords.y >= 0 and new_coords.x < len(elements[0]) and new_coords.y < len(elements):
        #     continue

        # print(coords, new_coords, list(itertools.islice(to_visit, 0, 5)))

        # elements = {}
        # for y in range(len(filled_map)):
        #     for x in range(len(filled_map[0])):
        #         elements[Point(x, y)] = filled_map[y][x]

        if check_coord_range(new_coords, elements) and elements[new_coords.y][new_coords.x] == target:
            closest = new_coords
            break

        if check_coord_range(new_coords, elements) and elements[new_coords.y][new_coords.x] != '.':
            continue

        # if new_coords in elements:
        #     continue

        for d in directions:
            coords_ = new_coords + d
            if coords_ not in previous_move:
                previous_move[coords_] = new_coords
                distance[coords_] = distance[new_coords] + 1

                to_visit.append(coords_)

    if closest is None:
        return None, None, None

    position = closest
    next_move = previous_move[closest]
    while next_move != coords:
        position = next_move
        next_move = previous_move[position]

    return closest, position, distance[closest]


def check_coord_range(coord, filled_map):
    return 0 <= coord.x < len(filled_map[0]) and 0 <= coord.y < len(filled_map)


def add_level(parent: Node, filled_map, potential_destinations):
    for descendant in [parent] + list(parent.descendants):
        if descendant.is_leaf:

            # print('Adding to: {}'.format(descendant.loc))

            for d in directions:
                new_coords = descendant.loc + d
                do_add = True
                # print('new_coordsing: {}'.format(new_coords))

                aa = set(find_accessible_areas_from_point(new_coords, filled_map, []))
                pds = list(set(potential_destinations) & aa)

                if len(pds) == 0:
                    continue

                if 0 <= new_coords.x < len(filled_map[0]) and 0 <= new_coords.y < len(filled_map) \
                        and filled_map[new_coords.y][new_coords.x] == '.':

                    # Don't immediately double back
                    if descendant.loc == new_coords:
                        continue

                    # Don't cross my tail
                    for a in [descendant] + list(descendant.ancestors):
                        if a.loc == new_coords:
                            do_add = False
                            break

                    if do_add is False:
                        continue

                    # Don't add a node if this spot has appeared
                    # anywhere in my siblings ancestors: ie: shorter distance
                    if descendant.parent:
                        for parent_sibling in descendant.parent.siblings:
                            for a in [parent_sibling] + list(parent_sibling.ancestors):
                                if a.loc == new_coords:
                                    do_add = False

                    if do_add:
                        Node(new_coords, descendant, loc=new_coords)


class Fighter:
    def __init__(self, x, y, type):
        self.loc = Point(x, y)
        self.hit_points = 200
        self.type = type

    def __repr__(self):
        return repr('{}: ({},{}) [{}]'.format(self.type, self.loc.x, self.loc.y, self.hit_points))

    def move(self, grid_map, fighters):
        if self.hit_points <= 0:
            return

        filled_map = fill_temp_map(fighters, grid_map)

        target = self.get_enemy()

        closest, next_coords, distance = find_closest_target(
            self.loc, target, filled_map
        )

        if next_coords is None:
            return

        if distance < 2:
            return

        old = self.loc
        self.loc = next_coords

    def _move(self, grid_map, fighters):
        if self.hit_points <= 0:
            return

        # Get ourselves a filled map and potential destinations
        filled_map = fill_temp_map(fighters, grid_map)
        pds = set(find_possible_destinations(self.loc, filled_map, filter_enemies(self, fighters)))
        aa = set(find_accessible_areas_from_point(self.loc, filled_map, []))
        pds = list(pds & aa)  # filter_possible_destinations(aa, pds)

        if len(pds) == 0:
            return

        # We're already in the right place
        if self.loc in pds:
            return

        top_of_tree = Node(self.loc, loc=self.loc)
        add_level(top_of_tree, filled_map, pds)

        last_len = len(top_of_tree.descendants)
        short_circuit_destination = None
        last_leaves = None
        while len(set(pds) & set(
                map(lambda d: d.loc, top_of_tree.descendants))) == 0 and short_circuit_destination is None:
            print('Height: {}, desc: {}'.format(top_of_tree.height, len(top_of_tree.descendants)))

            # print('')
            # for pre, fill, node in RenderTree(top_of_tree):
            #     print("%s%s" % (pre, node.name))

            curr_leaves = anytree_search.findall(top_of_tree,
                                                 filter_=lambda n: n.is_leaf and n.depth == top_of_tree.height)
            print('curr leaves: {}'.format(len(curr_leaves)))

            for leaf in curr_leaves:
                add_level(leaf, filled_map, pds)
                # print('')
                # for pre, fill, node in RenderTree(top_of_tree):
                #     print("%s%s" % (pre, node.name))

            if last_len == len(top_of_tree.descendants):
                # Couldn't find anywhere to try and go
                return
            elif top_of_tree.height != 1 and len(anytree_search.findall(top_of_tree, filter_=lambda
                    n: n.is_leaf and n.depth == top_of_tree.height)) == 1:
                short_circuit_destinationcircuit_destination = \
                anytree_search.findall(top_of_tree, filter_=lambda n: n.is_leaf, maxlevel=top_of_tree.height)[0]
            #     for pre, fill, node in RenderTree(top_of_tree):
            #         print("%s%s" % (pre, node.name))
            else:
                last_len = len(top_of_tree.descendants)

        # print('')
        # for pre, fill, node in RenderTree(top_of_tree):
        #     print("%s%s" % (pre, node.name))

        # Now let's find the correct path
        if short_circuit_destination:
            closest_points_we_can_reach = short_circuit_destination.loc
        else:
            closest_points_we_can_reach = set(pds) & set(map(lambda d: d.loc, top_of_tree.descendants))

        nodes = []
        depth = 0
        while len(nodes) == 0:
            depth += 1
            nodes = anytree_search.findall(top_of_tree, filter_=lambda n: n.loc in closest_points_we_can_reach,
                                           maxlevel=depth)

        best_path = None
        for path in nodes:
            if best_path is None:
                curr_path = list(path.ancestors) + [path]
                best_path = curr_path
            elif best_path[1].loc != select_by_reading_order(best_path[1].loc, curr_path[1].loc):
                best_path = curr_path

        # And finally move the fighter to the next square
        if best_path is not None:
            self.loc = best_path[1].loc

    #     for i in range(3):
    #         add_level(top_of_tree, filled_map)
    #
    #     print('')
    #     for pre, fill, node in RenderTree(top_of_tree):
    #         print("%s%s" % (pre, node.name))
    #
    #     # Special case if we are already in a potential destination position
    #     if self.loc in pds:
    #         return
    #
    #     aa = find_accessible_areas_from_point(self.loc, filled_map, [])
    #     pds = filter_possible_destinations(aa, pds)
    #
    #     # pds = sorted(pds, key=lambda p: manhattan_distance(self.loc, p))
    #
    #     dest_with_distance = {}
    #     for pd in pds:
    #         dest_with_distance[pd] = None
    #
    #     # Now find the shornew_coords or best path to an available enemy
    #     best_path_to_closest_enemy = None
    #     max_length = 100
    #     while len(pds) > 0:
    #         if best_path_to_closest_enemy is not None:
    #             max_length = len(best_path_to_closest_enemy)
    #         # else:
    #         #     max_length = min(manhattan_distance(self.loc, pd) * 3, max_length)
    #
    #         for pd in pds:
    #             if manhattan_distance(self.loc, pd) > max_length + 2:
    #                 pds.remove(pd)
    #
    #         # path = compute_best_path(self.loc, dest_with_distance, filled_map, deque(), max_length, 0)
    #         # if path:
    #         #
    #         # else:
    #         #     dest_with_distance.pop()
    #         #     break
    #
    #         # if best_path_to_closest_enemy is None:
    #         #     best_path_to_closest_enemy = path
    #         # elif len(path) < len(best_path_to_closest_enemy):
    #         #     best_path_to_closest_enemy = path
    #         # elif len(path) == len(best_path_to_closest_enemy):
    #         #     if best_path_to_closest_enemy[1] != select_by_reading_order(best_path_to_closest_enemy[1], path[1]):
    #         #         best_path_to_closest_enemy = path
    #
    #     # And finally move the fighter to the next square
    #     if best_path_to_closest_enemy is not None:
    #         self.loc = best_path_to_closest_enemy[1]
    #
    def attack(self, fighters):
        if self.hit_points <= 0:
            return

        potential_enemies = []
        for d in directions:
            for f in fighters:
                if f.loc == self.loc + d and self.enemy(f):
                    potential_enemies.append(f)

        # potential_enemies = list(filter(lambda f: f.loc in potential_locations and self.enemy(f) and f.hit_points > 0, fighters))
        enemies = sorted(potential_enemies, key=lambda f: f.hit_points)
        if len(enemies) > 0:
            enemies[0].hit_points -= 3

    def enemy(self, other):
        return self.type != other.type

    def get_enemy(self):
        if self.type == 'E':
            return 'G'
        else:
            return 'E'


def parse_map(entries):
    grid_map = []
    elves = []
    goblins = []

    for y in range(len(entries)):
        if len(list(entries[y])) == 0:
            break
        grid_map.append(list(entries[y]))

    for y in range(len(grid_map)):
        for x in range(len(grid_map[y])):
            if grid_map[y][x] == 'E':
                elves.append(Fighter(x, y, 'E'))
                grid_map[y][x] = '.'
            if grid_map[y][x] == 'G':
                goblins.append(Fighter(x, y, 'G'))
                grid_map[y][x] = '.'

    return grid_map, elves, goblins


def print_state(round, grid_map, elves, goblins):
    temp = fill_temp_map(elves + goblins, grid_map)

    print('Round: {}'.format(round))
    for row in temp:
        for v in row:
            print(v, end='')
        print('')
    print('')

    for f in elves + goblins:
        print(f)

    print('')


def fill_temp_map(fighters, grid_map):
    temp = deepcopy(grid_map)
    for f in fighters:
        if f.hit_points <= 0:
            continue
        temp[f.loc.y][f.loc.x] = f.type

    return temp


directions = [
    Point(0, -1),
    Point(-1, 0),
    Point(1, 0),
    Point(0, 1)
]


def filter_enemies(fighter, fighters):
    return filter(lambda f: fighter.enemy(f), fighters)


# First item in a computed path is always your starting square!
def compute_best_path(start: Point, destinations: List[Point], filled_map, visited, max_length=100, depth=0):
    depth += 1

    if FIGHTER.type == 'G' and FIGHTER.loc == Point(4, 2):
        # temp_map = fill_temp_map([Fighter(start.x, start.y, '*')], filled_map)
        # print_state('temp', temp_map, [], [])
        # print('.' * max(0, len(visited) - 10), end='')
        # print(list(itertools.islice(visited, max(0, len(visited) - 10), len(visited))))
        # print('depth : {}, visited: {}, max length: {}, current point: {}'.format(depth, len(visited), max_length, start))
        pass
    if len(visited) == 0:
        # This is a special case since we always start out where there is something!
        pass
    elif filled_map[start.y][start.x] != '.' or start in visited:
        return None

    # if len(visited) == 1:
    #     # Let's just make sure that we can reach our destination from here, the first legit non-start point
    #     aa = find_accessible_areas_from_point(start, filled_map, [])
    #     if dest not in aa:
    #         return None

    if len(visited) > max_length:
        return None

    visited.append(start)

    if start in destinations:
        destinations.remove(start)
        to_return = deepcopy(visited)
        visited.pop()
        return to_return

    shornew_coords_path = None

    # prioritized_directions = []
    # other_directions = []
    # absolute_distance = manhattan_distance(start, dest)

    # for d in directions:
    #     if manhattan_distance(start + d, dest) <= absolute_distance:
    #         prioritized_directions.append(d)
    #     else:
    #         other_directions.append(d)

    # directions_to_try = prioritized_directions
    # if len(directions_to_try) == 0:
    #     directions_to_try = other_directions

    for d in directions:
        if shornew_coords_path is not None:
            max_length = len(shornew_coords_path)

        path = compute_best_path(start + d, destinations, filled_map, visited, max_length, depth)

        if not path:
            continue

        if shornew_coords_path is None:
            shornew_coords_path = path
        elif len(path) < len(shornew_coords_path):
            shornew_coords_path = path
        elif len(path) == len(shornew_coords_path):
            if shornew_coords_path[1] != select_by_reading_order(shornew_coords_path[1], path[1]):
                shornew_coords_path = path

    # for d in other_directions:
    #     if shornew_coords_path is not None:
    #         max_length = len(shornew_coords_path)
    #
    #     path = compute_best_path(start + d, dest, filled_map, visited, max_length, depth)
    #
    #     if not path:
    #         continue
    #
    #     if shornew_coords_path is None:
    #         shornew_coords_path = path
    #     elif len(path) < len(shornew_coords_path):
    #         shornew_coords_path = path
    #     elif len(path) == len(shornew_coords_path):
    #         if shornew_coords_path[1] != select_by_reading_order(shornew_coords_path[1], path[1]):
    #             shornew_coords_path = path

    # if shornew_coords_path is None:
    visited.pop()

    depth -= 1
    return shornew_coords_path


def select_by_reading_order(p1: Point, p2: Point):
    return sorted([p1, p2], key=lambda p: (p.y, p.x))[0]


def filter_possible_destinations(accessible_areas, possible_destinations):
    temp_pds = []

    # Filter out destinations that are not reachable
    for pd in possible_destinations:
        if pd in accessible_areas:
            temp_pds.append(pd)

    return temp_pds


def find_possible_destinations(me, filled_map, enemies):
    possible_destinations = []

    # Find possible destinations
    for e in enemies:
        for d in directions:
            new_coords = e.loc + d

            if filled_map[new_coords.y][new_coords.x] == '.' or me == new_coords:
                possible_destinations.append(Point(new_coords.x, new_coords.y))

    return possible_destinations


def find_accessible_areas_from_point(start: Point, filled_map, already_known):
    if start not in already_known:
        already_known.append(start)
    for d in directions:
        new_coords = start + d
        if new_coords.x >= 0 and new_coords.y >= 0 and new_coords.x < len(filled_map[0]) and new_coords.y < len(
                filled_map) and \
                filled_map[new_coords.y][new_coords.x] == '.':
            new_point = Point(new_coords.x, new_coords.y)
            if new_point not in already_known:
                already_known.append(new_point)
                find_accessible_areas_from_point(new_point, filled_map, already_known=already_known)

    return already_known


def solve_15(input):
    entries = read_raw_entries(input)
    grid_map, elves, goblins = parse_map(entries)

    print_state(0, grid_map, elves, goblins)

    round = 0
    combat = True

    while combat:
        # print('Round: ' + str(round))
        # print_state(round, grid_map, elves, goblins)

        blah = 0
        for fighter in sort_fighters(elves, goblins):
            global FIGHTER
            FIGHTER = fighter

            # if FIGHTER.loc != Point(8,13):
            #     continue

            elves = list(filter(lambda e: e.hit_points > 0, elves))
            goblins = list(filter(lambda g: g.hit_points > 0, goblins))

            if len(elves) == 0 or len(goblins) == 0:
                combat = False
                break

            print('About to move: {}'.format(fighter), end='')
            sys.stdout.flush()
            fighter.move(grid_map, elves + goblins)
            print('.')
            # sys.stdout.flush()
            fighter.attack(elves + goblins)
            if round == 23:
                print_state('mid', grid_map, elves, goblins)

        print_state(round, grid_map, elves, goblins)
        # print('End')

        if combat:
            round += 1
            global ROUND
            ROUND = round

    hit_points = 0
    for f in elves + goblins:
        hit_points += f.hit_points

    return round * hit_points


def sort_fighters(elves, goblins):
    return sorted(elves + goblins, key=lambda f: (f.loc.y, f.loc.x))


if __name__ == '__main__':
    r = solve_15('input.txt')
    print(r)
