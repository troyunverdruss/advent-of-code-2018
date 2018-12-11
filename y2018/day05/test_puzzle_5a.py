from unittest import TestCase
from helpers.helpers import read_raw_entries
from y2018.day05.puzzle5ab import solve_5a, solve_5b, solve_try_1
import timeit

class TestSolve_5a(TestCase):
    def test_5a_1(self):
        self.assertEqual('', solve_5a('aA'))

    def test_5a_2(self):
        self.assertEqual('', solve_5a('abBA'))

    def test_5a_3(self):
        self.assertEqual('abAB', solve_5a('abAB'))

    def test_5a_4(self):
        self.assertEqual('aabAAB', solve_5a('aabAAB'))

    def test_solve_5a(self):
        polymer = 'dabAcCaCBAcCcaDA'
        r = solve_5a(polymer)

        self.assertEqual('dabCBAcaDA', r)

    def test_solve_5b(self):
        polymer = 'dabAcCaCBAcCcaDA'
        r = solve_5b(polymer)

        self.assertEqual(4, r)

    def test_perf(self):
        t = timeit.timeit(self.test_solve_5a, number=1000)
        print('Initial solution took: {}'.format(t))

        t = timeit.timeit(self.solve_try_1, number=1000)
        print('Time: {}'.format(t))

    def test_perf_2(self):
        t = timeit.timeit(self.do_work_1, number=1)
        print('Initial solution took: {}'.format(t))

        t = timeit.timeit(self.do_work_2, number=1)
        print('Time: {}'.format(t))

    def do_work_1(self):
        polymer = read_raw_entries('input.txt')[0]
        result = solve_5a(polymer)

    def do_work_2(self):
        polymer = read_raw_entries('input.txt')[0]
        result = solve_try_1(polymer)


    def solve_try_1(self):
        polymer = 'dabAcCaCBAcCcaDA'
        r = solve_try_1(polymer)

        self.assertEqual('dabCBAcaDA', r)
