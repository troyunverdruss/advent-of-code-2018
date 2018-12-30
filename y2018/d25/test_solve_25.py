from unittest import TestCase

from y2018.d25.puzzle_25 import solve_25, parse_input


class TestSolve_25(TestCase):
    def test_example_1(self):
        points = parse_input('test-input-1.txt')
        c = solve_25(points)
        self.assertEqual(2, c)

    def test_example_1_with_additional_point(self):
        points = parse_input('test-input-1-with-additional-point.txt')
        c = solve_25(points)
        self.assertEqual(1, c)

    def test_example_2(self):
        points = parse_input('test-input-2.txt')
        c = solve_25(points)
        self.assertEqual(4, c)

    def test_example_3(self):
        points = parse_input('test-input-3.txt')
        c = solve_25(points)
        self.assertEqual(3, c)

    def     test_example_4(self):
        points = parse_input('test-input-4.txt')
        c = solve_25(points)
        self.assertEqual(8, c)
