from unittest import TestCase
from y2018.d10.puzzle_10 import solve_10, read_stars

class TestSolve_10(TestCase):
    def test_example(self):
        stars = read_stars('test-input.txt')
        solve_10(stars)

