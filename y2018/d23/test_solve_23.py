from unittest import TestCase

from y2018.d23.puzzle_23 import parse_input, solve_23, solve_23_part_2


class TestSolve_23(TestCase):
    def test_example(self):
        nanobots = parse_input('test-input.txt')
        in_range = solve_23(nanobots)
        self.assertEqual(7, in_range)

    def test_mine_1(self):
        nanobots = parse_input('my-test-input.txt')
        in_range = solve_23_part_2(nanobots)
        self.assertEqual(7, in_range)

    def test_example_part_2(self):
        nanobots = parse_input('test-input-part-2.txt')
        distance = solve_23_part_2(nanobots)
        self.assertEqual(36, distance)
