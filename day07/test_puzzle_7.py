from unittest import TestCase
from helpers.helpers import read_raw_entries
from day07.puzzle_7a import process_into_steps, solve_7a
from typing import List


class TestSolve_7a(TestCase):
    def test_solve_7a(self):
        entries = read_raw_entries('test-input.txt')
        steps = process_into_steps(entries)
        r = solve_7a(steps)

        self.assertEqual('CABDFE', r)
