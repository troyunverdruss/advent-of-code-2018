from unittest import TestCase
from days.day14.puzzle_14 import solve_14a, solve_14b

class TestSolve_14(TestCase):
    def test_example_part_1_1(self):
        r = solve_14a(9)
        self.assertEqual('5158916779', r)

    def test_example_part_1_2(self):
        r = solve_14a(5)
        self.assertEqual('0124515891', r)

    def test_example_part_1_3(self):
        r = solve_14a(18)
        self.assertEqual('9251071085', r)

    def test_example_part_1_4(self):
        r = solve_14a(2018)
        self.assertEqual('5941429882', r)

    def test_example_part_2_1(self):
        r = solve_14b('51589')
        self.assertEqual(9, r)

    def test_example_part_2_2(self):
        r = solve_14b('01245')
        self.assertEqual(5, r)

    def test_example_part_2_3(self):
        r = solve_14b('92510')
        self.assertEqual(18, r)

    def test_example_part_2_4(self):
        r = solve_14b('59414')
        self.assertEqual(2018, r)
