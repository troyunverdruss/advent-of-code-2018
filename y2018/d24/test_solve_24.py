from unittest import TestCase

from y2018.d24.puzzle_24 import solve_24, parse_input


class TestSolve_24(TestCase):
    def test_example_1(self):
        armies = parse_input('test-input.txt')
        r = solve_24(armies)
        self.assertEqual(5216, r)
