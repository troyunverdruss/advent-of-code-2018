from unittest import TestCase
from y2018.d16.puzzle_16 import *


class TestSolve_16(TestCase):
    # mulr
    # addi
    # seti
    def test_0(self):
        # Before: [3, 2, 1, 1]
        # 9 2 1 2
        # After:  [3, 2, 2, 1]

        s = Sample((3, 2, 1, 1), (9, 2, 1, 2), (3, 2, 2, 1))
        r = find_match_count(s, limit=16)
        self.assertEqual(3, r)
        self.assertTrue(mulr.test(s))
        self.assertTrue(addi.test(s))
        self.assertTrue(seti.test(s))

    # addi
    # mulr
    # seti
    def test_1(self):
        s = Sample((3, 2, 1, 9), (9, 2, 1, 3), (3, 2, 1, 2))
        r = find_match_count(s, limit=16)
        self.assertEqual(3, r)
        self.assertTrue(addi.test(s))

    # addr
    # borr
    def test_2(self):
        s = Sample((3, 2, 1, 9), (9, 2, 1, 3), (3, 2, 1, 3))
        r = find_match_count(s, limit=16)
        self.assertEqual(2, r)
        self.assertTrue(addr.test(s))

    # muli
    def test_3(self):
        s = Sample((3, 2, 3, 1), (9, 2, 3, 3), (3, 2, 3, 9))
        r = find_match_count(s, limit=16)
        self.assertEqual(1, r)
        self.assertTrue(muli.test(s))

    # banr
    # seti
    def test_4(self):
        s = Sample((3, 2, 3, 1), (9, 2, 1, 3), (3, 2, 3, 2))
        r = find_match_count(s, limit=16)
        self.assertEqual(2, r)
        self.assertTrue(banr.test(s))

    # bani
    # seti
    def test_5(self):
        s = Sample((3, 2, 3, 1), (9, 2, 2, 3), (3, 2, 3, 2))
        r = find_match_count(s, limit=16)
        self.assertEqual(2, r)
        self.assertTrue(bani.test(s))

    # bori
    # addi
    def test_6(self):
        s = Sample((3, 2, 1, 1), (9, 2, 2, 3), (3, 2, 1, 3))
        r = find_match_count(s, limit=16)
        self.assertEqual(2, r)
        self.assertTrue(bori.test(s))

    # borr
    # mulr
    def test_6_1(self):
        s = Sample((3, 2, 1, 1), (9, 2, 0, 3), (3, 2, 1, 3))
        r = find_match_count(s, limit=16)
        self.assertEqual(2, r)
        self.assertTrue(borr.test(s))

    # setr
    # mulr
    # banr
    # borr
    # gtir
    # eqrr
    def test_7(self):
        s = Sample((3, 2, 1, 5), (9, 2, 2, 3), (3, 2, 1, 1))
        r = find_match_count(s, limit=16)
        self.assertEqual(6, r)
        self.assertTrue(setr.test(s))

    # gtir - not greater than, writes 0
    # muli
    # bani
    # gtrr
    # eqir
    # eqri
    # eqrr
    def test_8(self):
        s = Sample((3, 2, 1, 1), (9, 2, 0, 3), (3, 2, 1, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(7, r)
        self.assertTrue(gtir.test(s))

    # gtir - greater than, writes 1
    # gtri
    # gtrr
    def test_9(self):
        s = Sample((2, 2, 1, 4), (9, 3, 0, 3), (2, 2, 1, 1))
        r = find_match_count(s, limit=16)
        self.assertEqual(3, r)
        self.assertTrue(gtir.test(s))

    # gtir - writes 0 since equal
    # muli
    # bani
    # gtrr
    # eqri
    # eqrr
    def test_10(self):
        s = Sample((3, 2, 1, 1), (9, 3, 0, 3), (3, 2, 1, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(6, r)
        self.assertTrue(gtir.test(s))

    # gtri - not greater than, writes 0
    # bani
    # gtrr
    # eqir
    # eqri
    def test_11(self):
        s = Sample((3, 2, 1, 1), (9, 3, 2, 3), (3, 2, 1, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(5, r)
        self.assertTrue(gtri.test(s))

    # gtri - greater than, writes 1
    # gtrr
    # eqir
    def test_12(self):
        s = Sample((3, 2, 1, 4), (9, 3, 0, 3), (3, 2, 1, 1))
        r = find_match_count(s, limit=16)
        self.assertEqual(3, r)
        self.assertTrue(gtri.test(s))

    # gtri - equal, writes 0
    # banr
    # gtrr
    # eqir
    # eqrr
    def test_13(self):
        s = Sample((3, 2, 1, 1), (9, 3, 1, 3), (3, 2, 1, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(5, r)
        self.assertTrue(gtri.test(s))

    # seti
    # addr
    # borr
    def test_14(self):
        s = Sample((3, 2, 1, 1), (9, 3, 1, 3), (3, 2, 1, 3))
        r = find_match_count(s, limit=16)
        self.assertEqual(3, r)
        self.assertTrue(seti.test(s))

    # gtrr - not greater, writes 0
    # banr
    # gtri
    # eqir
    # eqrr
    def test_15(self):
        s = Sample((3, 2, 1, 1), (9, 3, 1, 3), (3, 2, 1, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(5, r)
        self.assertTrue(gtrr.test(s))

    # gtrr - equal, writes 0
    # gtri
    # eqir
    def test_16(self):
        s = Sample((3, 1, 2, 1), (9, 3, 1, 3), (3, 1, 2, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(3, r)
        self.assertTrue(gtrr.test(s))

    # gtrr - equal, writes 1
    # gtri
    # eqir
    def test_17(self):
        s = Sample((2, 3, 1, 4), (9, 3, 1, 3), (2, 3, 1, 1))
        r = find_match_count(s, limit=16)
        self.assertEqual(3, r)
        self.assertTrue(gtrr.test(s))

    # eqir - equal, set to 1
    # gtri
    # gtrr
    def test_18(self):
        s = Sample((2, 3, 1, 4), (9, 3, 1, 3), (2, 3, 1, 1))
        r = find_match_count(s, limit=16)
        self.assertEqual(3, r)
        self.assertTrue(eqir.test(s))

    # eqir - not equal set to 0
    # banr
    # bani
    # eqri
    # eqrr
    def test_19(self):
        s = Sample((2, 2, 1, 4), (9, 3, 1, 3), (2, 2, 1, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(5, r)
        self.assertTrue(eqir.test(s))

    # eqri - equal, set to 1
    # muli
    # banr
    # bani
    # bori
    # setr
    # eqir
    def test_20(self):
        s = Sample((2, 3, 1, 1), (9, 3, 1, 3), (2, 3, 1, 1))
        r = find_match_count(s, limit=16)
        self.assertEqual(7, r)
        self.assertTrue(eqri.test(s))

    # eqri - not equal, set to 0
    # banr
    # bani
    # gtir
    # eqri
    def test_21(self):
        s = Sample((2, 3, 1, 4), (9, 3, 1, 3), (2, 3, 1, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(5, r)
        self.assertTrue(eqri.test(s))

    # eqrr - equal set to 1
    # gtri
    def test_22(self):
        s = Sample((2, 4, 1, 4), (9, 3, 1, 3), (2, 4, 1, 1))
        r = find_match_count(s, limit=16)
        self.assertEqual(2, r)
        self.assertTrue(eqrr.test(s))

    # eqrr - not equal set to 0
    # banr
    # bani
    # gtir
    # eqri
    def test_23(self):
        s = Sample((2, 3, 1, 4), (9, 3, 1, 3), (2, 3, 1, 0))
        r = find_match_count(s, limit=16)
        self.assertEqual(5, r)
        self.assertTrue(eqrr.test(s))

    def test_24(self):
        s = Sample((0, 2, 1, 3), (1, 0, 0, 1), (0, 0, 1, 3))
        r = find_match_count(s, limit=16)
        self.assertEqual(13, r)
        self.assertTrue(gtir.test(s))
        self.assertTrue(gtri.test(s))
        self.assertTrue(gtrr.test(s))

        # gtir
        # gtri
        # gtrr
