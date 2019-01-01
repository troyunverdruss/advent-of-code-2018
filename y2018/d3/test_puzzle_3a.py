from unittest import TestCase
from y2018.d3.puzzle3ab import Claim, find_overlapping_square_inches, find_intact_claim


class TestClaim(TestCase):
    def test_parse_1(self):
        c = Claim()
        c.parse("#1 @ 2,3: 4x5")
        self.assertEqual(1, c.id)
        self.assertEqual(2, c.left)
        self.assertEqual(3, c.top)
        self.assertEqual(4, c.width)
        self.assertEqual(5, c.height)

    def test_get_overlap(self):
        raw_entries = [
            '#1 @ 1,3: 4x4',
            '#2 @ 3,1: 4x4',
            '#3 @ 5,5: 2x2'
        ]

        result = find_overlapping_square_inches(raw_entries)
        self.assertEqual(4, result)

    def test_find_intact_claim(self):
        raw_entries = [
            '#1 @ 1,3: 4x4',
            '#2 @ 3,1: 4x4',
            '#3 @ 5,5: 2x2'
        ]

        result = find_intact_claim(raw_entries)
        self.assertEqual(3, result)
