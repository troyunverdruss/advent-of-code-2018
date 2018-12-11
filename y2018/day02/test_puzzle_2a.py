from unittest import TestCase
from y2018.day02.puzzle2a import analyze, run_puzzle


class TestAnalyze(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAnalyze, self).__init__(*args, **kwargs)

        self.entries = [
            'abcdef',
            'bababc',
            'abbcde',
            'abcccd',
            'aabcdd',
            'abcdee',
            'ababab'
        ]

    def test_analyze_1(self):
        a = analyze(self.entries[0])
        self.assertEqual(0, a.pairs)
        self.assertEqual(False, a.has_pairs())
        self.assertEqual(0, a.triplets)
        self.assertEqual(False, a.has_triplets())

    def test_analyze_2(self):
        a = analyze(self.entries[1])
        self.assertEqual(1, a.pairs)
        self.assertEqual(True, a.has_pairs())
        self.assertEqual(1, a.triplets)
        self.assertEqual(True, a.has_triplets())

    def test_analyze_3(self):
        a = analyze(self.entries[2])
        self.assertEqual(1, a.pairs)
        self.assertEqual(True, a.has_pairs())
        self.assertEqual(0, a.triplets)
        self.assertEqual(False, a.has_triplets())

    def test_analyze_4(self):
        a = analyze(self.entries[3])
        self.assertEqual(0, a.pairs)
        self.assertEqual(False, a.has_pairs())
        self.assertEqual(1, a.triplets)
        self.assertEqual(True, a.has_triplets())

    def test_analyze_5(self):
        a = analyze(self.entries[4])
        self.assertEqual(2, a.pairs)
        self.assertEqual(True, a.has_pairs())
        self.assertEqual(0, a.triplets)
        self.assertEqual(False, a.has_triplets())

    def test_analyze_6(self):
        a = analyze(self.entries[5])
        self.assertEqual(1, a.pairs)
        self.assertEqual(True, a.has_pairs())
        self.assertEqual(0, a.triplets)
        self.assertEqual(False, a.has_triplets())

    def test_analyze_7(self):
        a = analyze(self.entries[6])
        self.assertEqual(0, a.pairs)
        self.assertEqual(False, a.has_pairs())
        self.assertEqual(2, a.triplets)
        self.assertEqual(True, a.has_triplets())

    def test_checksum(self):
        checksum = run_puzzle(self.entries)
        self.assertEqual(12, checksum)

