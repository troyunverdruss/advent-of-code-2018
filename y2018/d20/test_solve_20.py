from unittest import TestCase

from y2018.d20.puzzle_20 import solve_20


class TestSolve_20(TestCase):
    def test_sample_1(self):
        d = solve_20('^WNE$')
        self.assertEqual(3, d)

    def test_sample_2(self):
        d = solve_20('^ENWWW(NEEE|SSE(EE|N))$')
        self.assertEqual(10, d)

    def test_sample_3(self):
        d = solve_20('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')
        self.assertEqual(18, d)

    def test_mine_1(self):
        d = solve_20('^N(NES|)SS$')
        self.assertEqual(6, d)