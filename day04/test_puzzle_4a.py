from unittest import TestCase
from helpers.helpers import read_raw_entries
from day04.puzzle4ab import process_shifts, find_most_sleepy_guard, find_sleepiest_minute, solve_puzzle_4a, solve_puzzle_4b
import datetime


class TestProcess_shifts(TestCase):
    def test_process_shifts(self):
        entries = read_raw_entries('test-input.txt')

        shifts = process_shifts(entries)
        self.assertEqual(5, len(shifts))

        self.assertEqual(10, shifts[0].guard_id)
        self.assertEqual(datetime.date(1518, 11, 1), shifts[0].date)

        self.assertEqual(5, shifts[0].sleep_times[0].sleep_start)
        self.assertEqual(25, shifts[0].sleep_times[0].sleep_until)
        self.assertEqual(20, shifts[0].sleep_times[0].mins_asleep())

        self.assertEqual(30, shifts[0].sleep_times[1].sleep_start)
        self.assertEqual(55, shifts[0].sleep_times[1].sleep_until)
        self.assertEqual(25, shifts[0].sleep_times[1].mins_asleep())

        self.assertEqual(45, shifts[0].mins_asleep())

        self.assertEqual(list(range(5, 25)) + list(range(30, 55)), shifts[0].list_of_mins())

    def test_find_most_sleepy_guard(self):
        entries = read_raw_entries('test-input.txt')
        shifts = process_shifts(entries)

        guard, mins_asleep = find_most_sleepy_guard(shifts)

        self.assertEqual(10, guard)
        self.assertEqual(50, mins_asleep)

    def test_find_most_sleepy_minute(self):
        entries = read_raw_entries('test-input.txt')
        shifts = process_shifts(entries)

        guard, mins_asleep = find_most_sleepy_guard(shifts)

        min = find_sleepiest_minute(guard, shifts)

        self.assertEqual(24, min)

    def test_solve_puzzle_4a(self):
        entries = read_raw_entries('test-input.txt')

        guard_id, sleepiest_min = solve_puzzle_4a(entries)
        self.assertEqual(240, guard_id * sleepiest_min)

    def test_solve_puzzle_4b(self):
        entries = read_raw_entries('test-input.txt')
        guard_id, most_asleep_min = solve_puzzle_4b(entries)
        self.assertEqual(4455, guard_id * most_asleep_min)

