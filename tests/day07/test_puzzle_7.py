from unittest import TestCase
from helpers import read_raw_entries, path
from days.day07.puzzle_7ab import process_into_steps, solve_7a, solve_7b


class TestSolve_7a(TestCase):
    def test_solve_7a(self):
        entries = read_raw_entries(path(__file__, 'test-input.txt'))
        steps = process_into_steps(entries, 0)
        r = solve_7a(steps)

        self.assertEqual('CABDFE', r)

    def test_solve_7b(self):
        entries = read_raw_entries(path(__file__, 'test-input.txt'))
        steps = process_into_steps(entries, 0)
        r = solve_7b(steps, 2)

        self.assertEqual(15, r)
