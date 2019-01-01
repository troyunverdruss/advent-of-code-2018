from unittest import TestCase
from y2018.d11.puzzle_11 import solve_11, compute_cell
from helpers.helpers import Point

class TestSolve_11(TestCase):
    def test_compute_cell_1(self):
        v = compute_cell(Point(3, 5), 8)
        self.assertEqual(4, v)

    def test_compute_cell_2(self):
        v = compute_cell(Point(122,79), 57)
        self.assertEqual(-5, v)

    def test_compute_cell_3(self):
        v = compute_cell(Point(217, 196), 39)
        self.assertEqual(0, v)

    def test_compute_cell_4(self):
        v = compute_cell(Point(101, 153), 71)
        self.assertEqual(4, v)


    def test_1(self):
        r, dim = solve_11(18, 3, 3)
        self.assertEqual(33, r.x)
        self.assertEqual(45, r.y)

    def test_2(self):
        r, dim = solve_11(42, 3, 3)
        self.assertEqual(21, r.x)
        self.assertEqual(61, r.y)