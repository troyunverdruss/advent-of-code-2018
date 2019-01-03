from unittest import TestCase

from days.day23.puzzle_23 import parse_input, solve_23, solve_23_part_2
from helpers import path


class TestSolve_23(TestCase):
    def test_example(self):
        nanobots = parse_input(path(__file__, 'test-input.txt'))
        in_range = solve_23(nanobots)
        self.assertEqual(7, in_range)

    def test_example_part_2(self):
        nanobots = parse_input(path(__file__, 'test-input-part-2.txt'))
        distance = solve_23_part_2(nanobots)
        self.assertEqual(36, distance)
