from unittest import TestCase

from y2018.d23.puzzle_23 import parse_input, solve_23


class TestSolve_23(TestCase):
    def test_example(self):
        nanobots = parse_input('test-input.txt')
        in_range = solve_23(nanobots)
        self.assertEqual(7, in_range)
