from helpers import read_raw_entries, Point, path
from copy import deepcopy
import networkx as nx

ROUND = 0
FIGHTER = None


def find_closest_target(start, target_type, filled_map, enemies):
    possible_dests = find_possible_destinations(start, filled_map, enemies)
    aa = find_accessible_areas_from_point(start, filled_map, [])

    possible_dests = set(aa).intersection(set(possible_dests))

    # We're already where we want to go
    if start in possible_dests or len(possible_dests) == 0:
        return start, 1

    g = nx.Graph()
    for y in range(len(filled_map)):
        for x in range(len(filled_map[0])):
            if start == Point(x, y) or filled_map[y][x] == '.':
                for d in directions:
                    test = Point(x, y) + d
                    if filled_map[test.y][test.x] == '.':
                        g.add_edge(Point(x, y), test)

    shortest_path = 100_000
    new_location = None

    for pd in sorted(possible_dests, key=lambda p: (p.y, p.x)):
        if start in g and pd in g:
            try:
                path = nx.shortest_path(g, start, pd)
                if len(path) < shortest_path:
                    shortest_path = len(path)
                    new_location = path[1]
            except nx.NetworkXNoPath:
                pass

    if new_location is None:
        return start, 1

    return new_location, shortest_path


def check_coord_range(coord, filled_map):
    return 0 <= coord.x < len(filled_map[0]) and 0 <= coord.y < len(filled_map)


class Fighter:
    def __init__(self, x, y, type, attack_strength=3):
        self.loc = Point(x, y)
        self.hit_points = 200
        self.type = type
        self.attack_strength = attack_strength

    def __repr__(self):
        return repr('{}: ({},{}) [{}]'.format(self.type, self.loc.x, self.loc.y, self.hit_points))

    def move(self, grid_map, fighters):
        if self.hit_points <= 0:
            return

        enemies = list(filter(lambda f: f.type == self.get_enemy_type(), fighters))
        next_loc, distance = find_closest_target(self.loc, self.get_enemy_type(), fill_temp_map(fighters, grid_map),
                                                 enemies)

        if next_loc is None or distance < 2:
            return

        self.loc = next_loc

    def attack(self, fighters):
        if self.hit_points <= 0:
            return

        potential_enemies = []
        for d in directions:
            for f in fighters:
                if f.loc == self.loc + d and self.enemy(f):
                    potential_enemies.append(f)

        enemies = sorted(potential_enemies, key=lambda f: f.hit_points)
        if len(enemies) > 0:
            enemies[0].hit_points -= self.attack_strength

    def enemy(self, other):
        return self.type != other.type

    def get_enemy_type(self):
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
    pass
    # temp = fill_temp_map(elves + goblins, grid_map)
    #
    # print('Round: {}'.format(round))
    # for row in temp:
    #     for v in row:
    #         print(v, end='')
    #     print('')
    # print('')
    #
    # for f in elves + goblins:
    #     print(f)
    #
    # print('')


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


def solve_15(input_path, elf_strength=3, allow_elves_to_die=True):
    entries = read_raw_entries(input_path)
    grid_map, elves, goblins = parse_map(entries)

    total_elves = len(elves)
    for elf in elves:
        elf.attack_strength = elf_strength

    round = 0
    combat = True

    while combat:
        print_state(round, grid_map, elves, goblins)

        for fighter in sort_fighters(elves, goblins):

            elves = list(filter(lambda e: e.hit_points > 0, elves))
            goblins = list(filter(lambda g: g.hit_points > 0, goblins))

            if allow_elves_to_die is False and len(elves) != total_elves:
                combat = False
                break

            elif len(elves) == 0 or len(goblins) == 0:
                combat = False
                break

            fighter.move(grid_map, elves + goblins)
            fighter.attack(elves + goblins)

        if combat:
            round += 1

    hit_points = 0
    elf_count = 0
    for f in elves + goblins:
        hit_points += f.hit_points
        if f.type == 'E':
            elf_count += 1

    print_state(round, grid_map, elves, goblins)
    print('Elves: {}/{}. Rounds: {}, HP: {}, Total: {}'.format(elf_count, total_elves, round, hit_points,
                                                               round * hit_points))
    return round * hit_points, len(elves) == total_elves


def sort_fighters(elves, goblins):
    return sorted(elves + goblins, key=lambda f: (f.loc.y, f.loc.x))


if __name__ == '__main__':
    r, elves_survived = solve_15(path(__file__, 'input.txt'))
    print('Part 1: {}'.format(r))

    power = None
    for i in range(24, 200):
        power = i
        print('Trying power: {}'.format(i))
        r, elves_survived = solve_15(path(__file__, 'input.txt'), i, False)
        if elves_survived:
            break
        else:
            continue

    print('Part 2: {}, power: {}'.format(r, power))
