from unittest import TestCase
from y2018.d14.puzzle_14 import solve_14

class TestSolve_14(TestCase):
    def test_example_1(self):
        r = solve_14(9)
        self.assertEqual('5158916779', r)

    def test_example_2(self):
        r = solve_14(5)
        self.assertEqual('0124515891', r)

    def test_example_3(self):
        r = solve_14(18)
        self.assertEqual('9251071085', r)

    def test_example_4(self):
        r = solve_14(2018)
        self.assertEqual('5941429882', r)
