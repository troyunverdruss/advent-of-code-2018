from unittest import TestCase, skip

from helpers.helpers import Point
from days.day22.puzzle_22 import solve_22_part_1, solve_22_part_2


class TestSolve_22(TestCase):
    def test_example_part_1(self):
        r = solve_22_part_1(510, Point(10, 10))
        self.assertEqual(114, r)

    def test_example_part_2(self):
        r = solve_22_part_2(510, Point(10, 10))
        self.assertEqual(45, r)

