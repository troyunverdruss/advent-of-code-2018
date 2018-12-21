from unittest import TestCase

from y2018.d19.puzzle_19 import solve_19


class TestSolve_19(TestCase):
    def test_sample(self):
        r = solve_19('test-input.txt')
        self.assertEqual(6, r)
