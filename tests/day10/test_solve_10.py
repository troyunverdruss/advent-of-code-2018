from unittest import TestCase
from days.day10.puzzle_10 import solve_10, read_stars
from helpers import path


class TestSolve_10(TestCase):
    def test_example(self):
        stars = read_stars(path(__file__, 'test-input.txt'))
        solve_10(stars)

