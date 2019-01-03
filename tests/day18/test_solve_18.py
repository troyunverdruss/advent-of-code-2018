from unittest import TestCase

from helpers.helpers import read_raw_entries, path
from days.day18.puzzle_18 import solve_18


class TestSolve_18(TestCase):
    def test_sample(self):
        entries = read_raw_entries(path(__file__, 'test-input.txt'))
        r = solve_18(entries)
        self.assertEqual(1147, r)
