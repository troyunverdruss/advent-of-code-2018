from unittest import TestCase
from y2018.d15.puzzle_15 import solve_15, parse_map, Fighter, find_best_path, sort_fighters, print_state, \
    find_possible_destinations, find_accessible_areas_from_point, fill_temp_map, filter_enemies, \
    filter_possible_destinations, compute_best_path, select_by_reading_order
from helpers.helpers import read_raw_entries, Point


class Path:
    def __init__(self):
        self.nodes = []

    def __len__(self):
        return len(self.nodes)


class TestSolve_15(TestCase):
    def test_target_selection(self):
        entries = read_raw_entries('tests/target_selection/start_map.txt')
        grid_map, elves, goblins = parse_map(entries)

        print_state('Initial', grid_map, elves, goblins)

        i = 0
        for f in sort_fighters(elves, goblins):
            i += 1
            f.move(grid_map, elves + goblins)

            print_state('0.{}'.format(i), grid_map, elves, goblins)

    def test_movement(self):
        entries = read_raw_entries('tests/movement.txt')
        grid_map, elves, goblins = parse_map(entries)

        print_state('Initial', grid_map, elves, goblins)

        for i in range(5):
            j = 0
            for f in sort_fighters(elves, goblins):
                j += 1
                f.move(grid_map, elves + goblins)

                print_state('{}.{}'.format(i, j), grid_map, elves, goblins)

    def test_path_1(self):
        entries = read_raw_entries('tests/path-1.txt')
        entries = read_raw_entries('tests/path-1.txt')
        grid_map, elves, goblins = parse_map(entries)

        goblin = goblins[0]
        elf = elves[0]

        path = compute_best_path(goblin.loc, elf.loc, grid_map, [])

        x, y = goblin.loc.x, goblin.loc.y

        correct_path = [Point(x, y),
                        Point(x + 1, y), Point(x + 2, y), Point(x + 3, y),
                        Point(x + 4, y), Point(x + 5, y), Point(x + 6, y),
                        Point(x + 6, y + 1)]

        self.assertEqual(correct_path, path)

    def test_path_2(self):
        entries = read_raw_entries('tests/path-2.txt')
        grid_map, elves, goblins = parse_map(entries)

        goblin = goblins[0]
        elf = elves[0]

        path = compute_best_path(goblin.loc, elf.loc, grid_map, [])

        x, y = goblin.loc.x, goblin.loc.y

        correct_path = [Point(x, y),
                        Point(x + 1, y), Point(x + 2, y), Point(x + 2, y + 1),
                        Point(x + 3, y + 1), Point(x + 4, y + 1), Point(x + 5, y + 1),
                        Point(x + 6, y + 1)]

        self.assertEqual(correct_path, path)

    def test_path_3(self):
        entries = read_raw_entries('tests/path-3.txt')
        grid_map, elves, goblins = parse_map(entries)

        goblin = goblins[0]
        elf = elves[0]

        path = compute_best_path(goblin.loc, elf.loc, grid_map, [])

        x, y = goblin.loc.x, goblin.loc.y

        correct_path = [Point(x, y),
                        Point(x, y - 1), Point(x, y - 2), Point(x + 1, y - 2),
                        Point(x + 2, y - 2), Point(x + 3, y - 2), Point(x + 4, y - 2), Point(x + 5, y - 2),
                        Point(x + 6, y - 2)]

        self.assertEqual(correct_path, path)

    def test_1(self):
        r = solve_15('tests/sample-1.txt')
        self.assertEqual(590, r)

    def test_2(self):
        r = solve_15('tests/sample-2.txt')
        self.assertEqual(36334, r)

    def test_3(self):
        r = solve_15('tests/sample-3.txt')
        self.assertEqual(39514, r)

    def test_4(self):
        r = solve_15('tests/sample-4.txt')
        self.assertEqual(27755, r)

    def test_5(self):
        r = solve_15('tests/sample-5.txt')
        self.assertEqual(28944, r)

    def test_6(self):
        r = solve_15('tests/sample-6.txt')
        self.assertEqual(18740, r)
