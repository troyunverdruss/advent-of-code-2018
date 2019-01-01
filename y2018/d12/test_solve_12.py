from unittest import TestCase
from helpers.helpers import read_raw_entries
from y2018.d12.puzzle_12 import solve_12 as solve_12_bad, debug_difference
from y2018.d12.puzzle_12_try_2 import solve_12 as solve_12_good


class TestSolve_12(TestCase):
    def test_example_1(self):
        entries = read_raw_entries(__file__, 'test-input.txt')
        r = solve_12_good(entries)
        self.assertEqual(325, r)

    def test_debug_diff(self):
        debug_difference()
