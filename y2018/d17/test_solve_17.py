from unittest import TestCase

from y2018.d17.puzzle_17 import solve_17


class TestSolve_17(TestCase):
    def test_input(self):
        r = solve_17('test-input.txt')
        self.assertEqual(57, r)

    def test_edge_case(self):
        r = solve_17('edge-case-test.txt')
        self.assertEqual(472, r)
