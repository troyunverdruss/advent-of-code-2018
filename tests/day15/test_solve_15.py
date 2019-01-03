from unittest import TestCase, skip

from days.day15.puzzle_15 import solve_15, parse_map, sort_fighters, print_state, \
    find_accessible_areas_from_point, fill_temp_map
from helpers import read_raw_entries, Point, path


class Path:
    def __init__(self):
        self.nodes = []

    def __len__(self):
        return len(self.nodes)


class Testsolve_15(TestCase):
    @skip
    def test_target_selection(self):
        entries = read_raw_entries(path(__file__, 'tests/target_selection/start_map.txt'))
        grid_map, elves, goblins = parse_map(entries)

        print_state('Initial', grid_map, elves, goblins)

        i = 0
        for f in sort_fighters(elves, goblins):
            i += 1
            f.move(grid_map, elves + goblins)

            print_state('0.{}'.format(i), grid_map, elves, goblins)

    @skip
    def test_movement(self):
        entries = read_raw_entries(path(__file__, 'tests/movement.txt'))
        grid_map, elves, goblins = parse_map(entries)

        print_state('Initial', grid_map, elves, goblins)

        for i in range(5):
            j = 0
            for f in sort_fighters(elves, goblins):
                j += 1
                f.move(grid_map, elves + goblins)

                print_state('{}.{}'.format(i, j), grid_map, elves, goblins)

    def test_1(self):
        r, s = solve_15(path(__file__, 'tests/sample-1.txt'))
        self.assertEqual(27730, r)
        r, s = solve_15(path(__file__, 'tests/sample-1.txt'), 15, False)
        self.assertEqual(4988, r)

    @skip
    def test_blah(self):
        r = solve_15(path(__file__, 'tests/enemy-selection-1.txt'))
        self.assertEqual(27730, r)

    @skip
    def test_blah2(self):
        r = solve_15(path(__file__, 'tests/enemy-selection-2.txt'))
        self.assertEqual(27730, r)

    @skip
    def test_blah3(self):
        r = solve_15(path(__file__, 'tests/movement-2.txt'))
        self.assertEqual(27730, r)

    @skip
    def test_blah4(self):
        r = solve_15(path(__file__, 'tests/movement-3.txt'))
        self.assertEqual(27730, r)

    @skip
    def test_blah5(self):
        r = solve_15(path(__file__, 'tests/movement-4.txt'))
        self.assertEqual(27730, r)

    @skip
    def test_blah6(self):
        r = solve_15(path(__file__, 'tests/movement-5.txt'))
        self.assertEqual(27730, r)

    @skip
    def test_find_aa(self):
        # Should be 88 locations
        entries = read_raw_entries('tests/find-accessible-test.txt')
        grid_map, elves, goblins = parse_map(entries)
        filled_map = fill_temp_map(elves + goblins, grid_map)

        aa = find_accessible_areas_from_point(goblins[0].loc + Point(1, 0), filled_map, [])
        print(len(set(aa)))

        self.assertEqual(329, len(set(aa)))

    def test_2(self):
        r, s = solve_15(path(__file__, 'tests/sample-2.txt'))
        self.assertEqual(36334, r)

    def test_3(self):
        r, s = solve_15(path(__file__, 'tests/sample-3.txt'))
        self.assertEqual(39514, r)
        r, s = solve_15(path(__file__, 'tests/sample-3.txt'), 4, False)
        self.assertEqual(31284, r)

    def test_4(self):
        r, s = solve_15(path(__file__, 'tests/sample-4.txt'))
        self.assertEqual(27755, r)
        r, s = solve_15(path(__file__, 'tests/sample-4.txt'), 15, False)
        self.assertEqual(3478, r)

    def test_5(self):
        r, s = solve_15(path(__file__, 'tests/sample-5.txt'))
        self.assertEqual(28944, r)

        r, s = solve_15(path(__file__, 'tests/sample-5.txt'), 12, False)
        self.assertEqual(6474, r)

    def test_6(self):
        r, s = solve_15(path(__file__, 'tests/sample-6.txt'))
        self.assertEqual(18740, r)
        r, s = solve_15(path(__file__, 'tests/sample-6.txt'), 34, False)
        self.assertEqual(1140, r)

    @skip
    def test_real_part_1(self):
        r, s = solve_15(path(__file__, 'input.txt'))
        self.assertEqual(227290, r)

    @skip
    def test_real_part_2(self):
        r, s = solve_15(path(__file__, 'input.txt'), elf_strength=25, allow_elves_to_die=False)
        self.assertEqual(53725, r)
