from unittest import TestCase
from day06.puzzle6ab import solve_6a, convert_points, manhattan_distance, solve_6b
from helpers.helpers import read_raw_entries


class TestSolve_6a(TestCase):
    def test_solve_6a(self):
        entries = read_raw_entries('test-input.txt')
        points = convert_points(entries)

        r = solve_6a(points)
        self.assertEqual(17, r)

    def test_solve_6b(self):
        entries = read_raw_entries('test-input.txt')
        points = convert_points(entries)

        r = solve_6b(points, 32)
        self.assertEqual(16, r)

    def test_convert_points(self):
        entries = ['1, 2', '3, 4']
        points = convert_points(entries)

        self.assertEqual(2, len(points))

        self.assertEqual(1, points[0].x)
        self.assertEqual(2, points[0].y)

        self.assertEqual(3, points[1].x)
        self.assertEqual(4, points[1].y)


    def test_manhattan_distance_1(self):
        entries = ['1, 2', '3, 4']
        points = convert_points(entries)

        d = manhattan_distance(points[0], points[1])

        self.assertEqual(4, d)

    def test_manhattan_distance_2(self):
        entries = ['1, 1', '1, 4']
        points = convert_points(entries)

        d = manhattan_distance(points[0], points[1])

        self.assertEqual(3, d)

    def test_manhattan_distance_3(self):
        entries = ['1, 1', '4, 4']
        points = convert_points(entries)

        d = manhattan_distance(points[0], points[1])

        self.assertEqual(6, d)

    def test_manhattan_distance_4(self):
        entries = ['1, 1', '1, 1']
        points = convert_points(entries)

        d = manhattan_distance(points[0], points[1])

        self.assertEqual(0, d)
