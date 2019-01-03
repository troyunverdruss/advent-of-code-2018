from helpers.helpers import read_raw_entries, path
import re
import datetime
from collections import Counter


class SleepTime:
    def __init__(self):
        self.sleep_start = None
        self.sleep_until = None

    def mins_asleep(self):
        return self.sleep_until - self.sleep_start

    def list_of_mins(self):
        return list(range(self.sleep_start, self.sleep_until))


class GuardShift:
    def __init__(self):
        self.guard_id = None
        self.date = None

        self.sleep_times = []
        self.cached_mins_asleep = None

    def add_sleep_time(self, sleep_time):
        self.cached_mins_asleep = None
        self.sleep_times.append(sleep_time)

    def mins_asleep(self):
        total = 0
        for sleep_time in self.sleep_times:
            total += sleep_time.mins_asleep()

        return total

    def list_of_mins(self):
        list_of_mins = []
        for sleep_time in self.sleep_times:
            list_of_mins += sleep_time.list_of_mins()

        return list_of_mins


def process_shifts(entries):
    guard_on_duty = None

    # Get first guard on duty
    e = entries.pop(0)

    # regex for guard begin shift
    guard_pattern = re.compile('^\[(\d+)\-(\d+)\-(\d+)\s+(\d+):(\d+)\]\s+Guard\s+#(\d+)\s+begins\s+shift$')
    falls_asleep_pattern = re.compile('^\[(\d+)\-(\d+)\-(\d+)\s+(\d+):(\d+)\]\s+falls\s+asleep$')
    wakes_up_pattern = re.compile('^\[(\d+)\-(\d+)\-(\d+)\s+(\d+):(\d+)\]\s+wakes\s+up$')

    matcher = guard_pattern.match(e)
    guard_on_duty = int(matcher.group(6))

    shifts = []

    shift = GuardShift()
    shift.guard_id = guard_on_duty
    sleep_time = SleepTime()

    for e in entries:
        if sleep_time.sleep_start is None:
            matcher = falls_asleep_pattern.match(e)
            if matcher:
                shift.date = datetime.date(int(matcher.group(1)), int(matcher.group(2)), int(matcher.group(3)))
                sleep_time.sleep_start = int(matcher.group(5))
            else:
                matcher = guard_pattern.match(e)
                if matcher:
                    shifts.append(shift)
                    shift = GuardShift()
                    shift.guard_id = int(matcher.group(6))
        else:
            matcher = wakes_up_pattern.match(e)
            if matcher:
                sleep_time.sleep_until = int(matcher.group(5))
                shift.sleep_times.append(sleep_time)
                sleep_time = SleepTime()

    shifts.append(shift)
    return shifts


def find_most_sleepy_guard(shifts):
    mins_asleep = {}
    for shift in shifts:
        if shift.guard_id not in mins_asleep:
            mins_asleep[shift.guard_id] = 0

        mins_asleep[shift.guard_id] += shift.mins_asleep()
    guard_id = max(mins_asleep, key=mins_asleep.get)
    return guard_id, mins_asleep[guard_id]


def find_sleepiest_minute_with_count(guard_id, shifts):
    all_mins = []

    for shift in shifts:
        if shift.guard_id != guard_id:
            continue

        all_mins += shift.list_of_mins()

    data = Counter(all_mins)
    if len(all_mins) == 0:
        return (0, 0)

    return data.most_common(1)[0]


def find_sleepiest_minute(guard_id, shifts):
    return find_sleepiest_minute_with_count(guard_id, shifts)[0]


def solve_puzzle_4a(entries):
    shifts = process_shifts(entries)

    guard_id, mins_asleep = find_most_sleepy_guard(shifts)
    sleepiest_min = find_sleepiest_minute(guard_id, shifts)

    return guard_id, sleepiest_min


def solve_puzzle_4b(entries):
    shifts = process_shifts(entries)
    guards = set(map(lambda s: s.guard_id, shifts))

    guard_id = 0
    minute = None
    count = 0

    for guard in guards:
        min_with_count = find_sleepiest_minute_with_count(guard, shifts)
        if min_with_count[1] > count:
            guard_id = guard
            minute = min_with_count[0]
            count = min_with_count[1]

    return guard_id, minute


if __name__ == '__main__':
    entries = read_raw_entries(path(__file__, 'input-sorted.txt'))
    guard_id, sleepiest_min = solve_puzzle_4a(entries)
    print('Guard ID: {}, sleepiest min: {}, checksum: {}'.format(guard_id, sleepiest_min, guard_id * sleepiest_min))

    entries = read_raw_entries(path(__file__, 'input-sorted.txt'))
    guard_id, minute = solve_puzzle_4b(entries)
    print('Guard ID: {}, sleepiest min: {}, checksum: {}'.format(guard_id, minute, guard_id * minute))

