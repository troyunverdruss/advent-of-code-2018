from unittest import TestCase
from y2017.d1.puzzle_1 import solve_1


class TestSolve_1(TestCase):
    def test_1(self):
        input = '1122'
        r = solve_1(input)
        self.assertEqual(3, r)

    def test_2(self):
        input = '1111'
        r = solve_1(input)
        self.assertEqual(4, r)

    def test_3(self):
        input = '1234'
        r = solve_1(input)
        self.assertEqual(0, r)

    def test_4(self):
        input = '91212129'
        r = solve_1(input)
        self.assertEqual(9, r)

    def test_5(self):
        input = '1212'
        r = solve_1(input, 2)
        self.assertEqual(6, r)

    def test_6(self):
        input = '1221'
        r = solve_1(input, 2)
        self.assertEqual(0, r)

    def test_7(self):
        input = '123425'
        r = solve_1(input, 3)
        self.assertEqual(4, r)

    def test_8(self):
        input = '123123'
        r = solve_1(input, 3)
        self.assertEqual(12, r)

    def test_8(self):
        input = '12131415'
        r = solve_1(input, 4)
        self.assertEqual(4, r)
