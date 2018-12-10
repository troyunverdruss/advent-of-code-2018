from unittest import TestCase
from day09.puzzle_9 import solve_9a, Circle


class TestSolve9(TestCase):
    def test_1(self):
        input = '10 players; last marble is worth 1618 points'
        r = solve_9a(input)
        self.assertEqual(8317, r)

    def test_2(self):
        input = '13 players; last marble is worth 7999 points'
        r = solve_9a(input)
        self.assertEqual(146373, r)

    def test_3(self):
        input = '17 players; last marble is worth 1104 points'
        r = solve_9a(input)
        self.assertEqual(2764, r)

    def test_4(self):
        input = '21 players; last marble is worth 6111 points'
        r = solve_9a(input)
        self.assertEqual(54718, r)

    def test_5(self):
        input = '30 players; last marble is worth 5807 points'
        r = solve_9a(input)
        self.assertEqual(37305, r)

    def test_6(self):
        input = '9 players; last marble is worth 25 points'
        r = solve_9a(input)
        self.assertEqual(32, r)

    def test_subtract_7_over_0(self):
        v = self.do_subtraction(9, 10)
        self.assertEqual(2, v)

        v = self.do_subtraction(8, 10)
        self.assertEqual(1, v)

        v = self.do_subtraction(1, 10)
        self.assertEqual(4, v)

        v = self.do_subtraction(2, 10)
        self.assertEqual(5, v)

        v = self.do_subtraction(3, 10)
        self.assertEqual(6, v)

        v = self.do_subtraction(4, 10)
        self.assertEqual(7, v)

        v = self.do_subtraction(5, 10)
        self.assertEqual(8, v)

        v = self.do_subtraction(6, 10)
        self.assertEqual(9, v)

        v = self.do_subtraction(7, 10)
        self.assertEqual(0, v)

    def do_subtraction(self, start: int, circle_size: int) -> int:
        new_active = None

        new_active = (start - 7) % circle_size

        return new_active

    def test_board_matches(self):
        expected_board_entries = [
            '(0) ',
            '0 (1) ',
            '0 (2) 1 ',
            '0 2 1 (3) ',
            '0 (4) 2 1 3 ',
            '0 4 2 (5) 1 3 ',
            '0 4 2 5 1 (6) 3 ',
            '0 4 2 5 1 6 3 (7) ',
            '0 (8) 4 2 5 1 6 3 7 ',
            '0 8 4 (9) 2 5 1 6 3 7 ',
            '0 8 4 9 2 (10) 5 1 6 3 7 ',
            '0 8 4 9 2 10 5 (11) 1 6 3 7 ',
            '0 8 4 9 2 10 5 11 1 (12) 6 3 7 ',
            '0 8 4 9 2 10 5 11 1 12 6 (13) 3 7 ',
            '0 8 4 9 2 10 5 11 1 12 6 13 3 (14) 7 ',
            '0 8 4 9 2 10 5 11 1 12 6 13 3 14 7 (15) ',
            '0 (16) 8 4 9 2 10 5 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 (17) 4 9 2 10 5 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 17 4 (18) 9 2 10 5 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 17 4 18 9 (19) 2 10 5 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 17 4 18 9 19 2 (20) 10 5 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 17 4 18 9 19 2 20 10 (21) 5 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 17 4 18 9 19 2 20 10 21 5 (22) 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 17 4 18 (19) 2 20 10 21 5 22 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 17 4 18 19 2 (24) 20 10 21 5 22 11 1 12 6 13 3 14 7 15 ',
            '0 16 8 17 4 18 19 2 24 20 (25) 10 21 5 22 11 1 12 6 13 3 14 7 15 '
        ]

        circle = Circle()
        marble_value = 1

        while marble_value <= 25:
            print('marble value: {}'.format(marble_value))

            score, string_rep = circle.add_marble(marble_value)
            print(string_rep)

            self.assertEqual(string_rep, expected_board_entries[marble_value])
            marble_value += 1

