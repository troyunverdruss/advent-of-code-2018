from unittest import TestCase
from day05.puzzle5a import solve_5a, solve_5b


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

