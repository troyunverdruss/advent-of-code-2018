from unittest import TestCase
from day02.puzzle2b import diff_count, get_common, is_diff_one, run_puzzle


class TestDiff_count(TestCase):

    def test_compare_1(self):
        a = 'abcde'
        b = 'axcye'

        r = diff_count(a, b)
        self.assertEqual(2, r)

        r = is_diff_one(a, b)
        self.assertEqual(False, r)

    def test_compare_2(self):
        a = 'fghij'
        b = 'fguij'

        r = diff_count(a, b)
        self.assertEqual(1, r)

        r = is_diff_one(a, b)
        self.assertEqual(True, r)

    def test_compare_3(self):
        a = 'abcde'
        b = 'lkjhg'

        r = diff_count(a, b)
        self.assertEqual(5, r)

        r = is_diff_one(a, b)
        self.assertEqual(False, r)

    def test_compare_4(self):
        a = 'abcde'
        b = 'abcde'

        r = diff_count(a, b)
        self.assertEqual(0, r)

        r = is_diff_one(a, b)
        self.assertEqual(False, r)

    def test_common_1(self):
        a = 'abcde'
        b = 'axcye'

        r = get_common(a, b)
        self.assertEqual('ace', r)

    def test_common_2(self):
        a = 'fghij'
        b = 'fguij'

        r = get_common(a, b)
        self.assertEqual('fgij', r)

    def test_common_3(self):
        a = 'abcde'
        b = 'lkjhg'

        r = get_common(a, b)
        self.assertEqual('', r)

    def test_common_4(self):
        a = 'abcde'
        b = 'abcde'

        r = get_common(a, b)
        self.assertEqual('abcde', r)

    def test_get_common(self):
        entries = [
            'abcde',
            'fghij',
            'klmno',
            'pqrst',
            'fguij',
            'axcye',
            'wvxyz'
        ]

        result = run_puzzle(entries)
        self.assertEqual('fgij', result)
