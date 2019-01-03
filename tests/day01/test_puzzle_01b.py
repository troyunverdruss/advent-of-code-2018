from unittest import TestCase
from days.day01.puzzle01b import run_puzzle
from helpers import path


class TestPuzzle(TestCase):
    def test_puzzle_sample_1(self):
        r = run_puzzle(path(__file__,'test-data/01b-sample-1.txt'))
        self.assertEqual(0, r)

    def test_puzzle_sample_2(self):
        r = run_puzzle(path(__file__,'test-data/01b-sample-2.txt'))
        self.assertEqual(10, r)

    def test_puzzle_sample_3(self):
        r = run_puzzle(path(__file__,'test-data/01b-sample-3.txt'))
        self.assertEqual(5, r)

    def test_puzzle_sample_4(self):
        r = run_puzzle(path(__file__,'test-data/01b-sample-4.txt'))
        self.assertEqual(14, r)
