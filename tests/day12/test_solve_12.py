from unittest import TestCase
from helpers import read_raw_entries, path
from days.day12.puzzle_12_try_2 import solve_12 as solve_12_good


class TestSolve_12(TestCase):
    def test_example_1(self):
        entries = read_raw_entries(path(__file__, 'test-input.txt'))
        r = solve_12_good(entries)
        self.assertEqual(325, r)
