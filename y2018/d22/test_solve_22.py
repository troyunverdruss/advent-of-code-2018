from unittest import TestCase, skip

from helpers.helpers import Point
from y2018.d22.puzzle_22 import solve_22


class TestSolve_22(TestCase):
    def test_example(self):
        r = solve_22(510, Point(10,10))
        self.assertEqual(114, r)

    @skip
    def test_mine_1(self):
        r = solve_22(510, Point(2, 5))
        self.assertEqual(114, r)
