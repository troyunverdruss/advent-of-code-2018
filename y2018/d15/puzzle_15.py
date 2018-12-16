from helpers.helpers import read_raw_entries, Point, manhattan_distance
from copy import deepcopy


class Fighter:
    def __init__(self, x, y, type):
        self.loc = Point(x, y)
        self.hit_points = 200
        self.type = type

    def __repr__(self):
        return repr('{}: ({},{}) [{}]'.format(self.type, self.loc.x, self.loc.y, self.hit_points))

    def move(self, grid_map, fighters):
        # Get ourselves a filled map and potential destinations
        filled_map = fill_temp_map(fighters, grid_map)
        pds = find_possible_destinations(self.loc, filled_map, filter_enemies(self, fighters))

        # Special case if we are already in a potential destination position
        if self.loc in pds:
            return

        aa = find_accessible_areas_from_point(self.loc, filled_map, [])
        pds = filter_possible_destinations(aa, pds)

        # Now find the shortest or best path to an available enemy
        best_path_to_closest_enemy = None
        for pd in pds:
            path = compute_best_path(self.loc, pd, filled_map, [])
            if not path:
                continue

            if best_path_to_closest_enemy is None:
                best_path_to_closest_enemy = path
            elif len(path) < len(best_path_to_closest_enemy):
                best_path_to_closest_enemy = path
            elif len(path) == len(best_path_to_closest_enemy):
                if best_path_to_closest_enemy[1] != select_by_reading_order(best_path_to_closest_enemy[1], path[1]):
                    best_path_to_closest_enemy = path

        # And finally move the fighter to the next square
        if best_path_to_closest_enemy is not None:
            self.loc = best_path_to_closest_enemy[1]

    def attack(self, elves, goblins):
        pass

    def enemy(self, other):
        return self.type != other.type


def parse_map(entries):
    grid_map = []
    elves = []
    goblins = []

    for y in range(len(entries)):
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


def find_best_path(start: Point, dest: Point, filled_map):
    pass


def filter_enemies(fighter, fighters):
    return filter(lambda f: fighter.enemy(f), fighters)


def find_dest_point(fighter: Fighter, filled_map, fighters):
    enemies = filter_enemies(fighter, fighters)

    possible_destinations = find_possible_destinations(filled_map, enemies)

    accessible_areas = find_accessible_areas_from_point(fighter.loc, filled_map, [])

    possible_destinations = filter_possible_destinations(accessible_areas, possible_destinations)

    nearest_areas = find_nearest_areas


# First item in a computed path is always your starting square!
def compute_best_path(start: Point, dest: Point, filled_map, visited):
    if len(visited) == 0:
        # This is a special case since we always start out where there is something!
        pass
    elif filled_map[start.y][start.x] != '.' or start in visited:
        return None

    visited.append(start)

    if start == dest:
        return visited

    shortest_path = None

    prioritized_directions = []
    other_directions = []
    absolute_distance = manhattan_distance(start, dest)
    for d in directions:
        if manhattan_distance(start + d, dest) <= absolute_distance:
            prioritized_directions.append(d)
        else:
            other_directions.append(d)

    directions_to_try = prioritized_directions
    if len(directions_to_try) == 0:
        directions_to_try = other_directions

    for d in directions_to_try:
        path = compute_best_path(start + d, dest, filled_map, deepcopy(visited))

        if not path:
            continue

        if shortest_path is None:
            shortest_path = path
        elif len(path) < len(shortest_path):
            shortest_path = path

    return shortest_path


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
            test = e.loc + d

            if filled_map[test.y][test.x] == '.' or me == test:
                possible_destinations.append(Point(test.x, test.y))

    return possible_destinations


def find_accessible_areas_from_point(start: Point, filled_map, already_known):
    for d in directions:
        test = start + d
        if filled_map[test.y][test.x] == '.':
            new_point = Point(test.x, test.y)
            if new_point not in already_known:
                already_known.append(new_point)
                find_accessible_areas_from_point(new_point, filled_map, already_known=already_known)

    return already_known


def solve_15(input):
    entries = read_raw_entries(input)
    grid_map, elves, goblins = parse_map(entries)

    print_state(0, grid_map, elves, goblins)

    round = 1
    combat = True

    while combat:
        for fighter in sort_fighters(elves, goblins):
            fighter.move(grid_map, elves + goblins)
            fighter.attack(elves, goblins)

        if combat:
            round += 1

    i = 0


def sort_fighters(elves, goblins):
    return sorted(elves + goblins, key=lambda f: (f.loc.y, f.loc.x))


if __name__ == '__main__':
    pass
