from unittest import TestCase

from helpers import read_raw_entries, path
from days.day24.puzzle_24 import solve_24, parse_input, ArmyGroup


class TestSolve_24(TestCase):
    def test_example_1(self):
        entries = read_raw_entries(path(__file__, 'test-input.txt'))
        armies = parse_input(entries)
        r, imm_system_wins = solve_24(armies)
        self.assertEqual(5216, r)
        self.assertFalse(imm_system_wins)

    def test_example_2_with_boost(self):
        entries = read_raw_entries(path(__file__, 'test-input.txt'))
        armies = parse_input(entries)
        r, imm_system_wins = solve_24(armies, 1570)
        self.assertEqual(51, r)
        self.assertTrue(imm_system_wins)

    def test_parse_1(self):
        s = [
            'Immune System:',
            '1590 units each with 3940 hit points with an attack that does 24 cold damage at initiative 5'
        ]
        armies = parse_input(s)
        self.assertEqual(len(armies), 1)
        self.assertEqual(
            ArmyGroup(0, 1, 'imm', 1590, 3940, [], [], 24, 'cold', 5),
            armies[0]
        )

    def test_parse_2(self):
        s = [
            'Infection:',
            '6792 units each with 6242 hit points (immune to slashing; weak to bludgeoning, radiation) with an attack that does 9 slashing damage at initiative 18'
        ]
        armies = parse_input(s)
        self.assertEqual(len(armies), 1)
        self.assertEqual(
            ArmyGroup(0, 1, 'inf', 6792, 6242, ['bludgeoning', 'radiation'], ['slashing'], 9, 'slashing', 18),
            armies[0]
        )
