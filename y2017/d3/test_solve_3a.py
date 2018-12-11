from unittest import TestCase
from y2017.d3.puzzle_3 import solve_3a


class TestSolve_3a(TestCase):
    def test_1(self):
        r = solve_3a(1)
        self.assertEqual(0, r)

    def test_2(self):
        r = solve_3a(12)
        self.assertEqual(3, r)

    def test_3(self):
        r = solve_3a(23)
        self.assertEqual(2, r)

    def test_4(self):
        r = solve_3a(1024)
        self.assertEqual(31, r)