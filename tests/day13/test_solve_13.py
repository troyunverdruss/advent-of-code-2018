from unittest import TestCase
from days.day13.puzzle_13 import solve_13
from helpers.helpers import path


class TestSolve_13(TestCase):
    def test_first_collision(self):
        r = solve_13(path(__file__, 'test-input-find-first-collision.txt'))
        self.assertEqual(7, r.x)
        self.assertEqual(3, r.y)

    def test_last_cart_standing(self):
        r = solve_13(path(__file__, 'test-input-find-last-cart-standing.txt'), True)
        self.assertEqual(6, r.x)
        self.assertEqual(4, r.y)
