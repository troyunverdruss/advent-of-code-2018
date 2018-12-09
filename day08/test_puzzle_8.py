from unittest import TestCase
from day08.puzzle_8 import solve_8a


class TestPuzzle8(TestCase):
    def test_solve_8a(self):
        input = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
        r = solve_8a(input)
        self.assertEqual(138, r)
