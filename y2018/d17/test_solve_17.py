from unittest import TestCase

from helpers.helpers import read_raw_entries, Point
from y2018.d17.puzzle_17 import parse_real_input
from y2018.d17.puzzle_17_try_2 import solve_17


class TestSolve_17(TestCase):
    def test_input(self):
        points = parse_real_input('test-input.txt')
        r = solve_17(points)
        self.assertEqual(57, r)

    def test_input(self):
        points = parse_real_input('test-input.txt')
        r = solve_17(points,  still=True)
        self.assertEqual(29, r)

    def test_edge_case(self):
        points = parse_real_input('edge-cases/1.txt')
        r = solve_17(points)
        self.assertEqual(472, r)

    def test_edge_case_2(self):
        points = parse_real_input('edge-cases/2.txt')
        r = solve_17(points)
        self.assertEqual(628, r)

    def test_3(self):
        points = self.parse_ascii_input('edge-cases/3.txt')
        r = solve_17(points)
        self.assertEqual(47, r)

    def test_4(self):
        points = self.parse_ascii_input('edge-cases/4.txt')
        r = solve_17(points)
        self.assertEqual(8, r)

    def test_5(self):
        points = self.parse_ascii_input('edge-cases/5.txt')
        r = solve_17(points)
        self.assertEqual(8, r)

    def test_6(self):
        points = self.parse_ascii_input('edge-cases/6.txt')
        r = solve_17(points)
        self.assertEqual(213, r)

    def test_7(self):
        points = self.parse_ascii_input('edge-cases/7.txt')
        r = solve_17(points)
        self.assertEqual(177, r)

    def parse_ascii_input(self, input):
        entries = read_raw_entries(__file__, input)
        points = []
        grid = []
        for entry in entries:
            grid.append(list(entry))

        width = len(grid[0])
        left = 500 - (width // 2)

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == '#':
                    points.append(Point(left + x, y + 1))

        return points
