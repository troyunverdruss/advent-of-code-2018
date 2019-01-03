from unittest import TestCase

from days.day19.puzzle_19 import solve_19
from helpers.helpers import path


class TestSolve_19(TestCase):
    def test_sample(self):
        r = solve_19(path(__file__, 'test-input.txt'))
        self.assertEqual(6, r)
