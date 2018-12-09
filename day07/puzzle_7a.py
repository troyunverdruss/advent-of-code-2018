from helpers.helpers import read_raw_entries
from typing import List, Dict
import re
import string


class Step:
    def __init__(self):
        self.prereqs = []


def process_into_steps(entries):
    steps = {}



    p = re.compile(r'^Step (\w) must be finished before step (\w) can begin.$')

    for entry in entries:
        matcher = p.match(entry.strip())

        if not matcher:
            raise Exception('Entry could not be parsed! {}'.format(entry))

        if matcher.group(1) not in steps:
            steps[matcher.group(1)] = Step()

        if matcher.group(2) not in steps:
            steps[matcher.group(2)] = Step()

        steps[matcher.group(2)].prereqs.append(matcher.group(1))

    return steps


def solve_7a(steps: Dict[str, Step]):
    pending_steps = sorted(steps)
    finished_steps = []

    while len(pending_steps) > 0:
        for step in pending_steps:
            if all(s in finished_steps for s in steps[step].prereqs):
                pending_steps.remove(step)
                finished_steps.append(step)
                break

    return ''.join(finished_steps)


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    steps = process_into_steps(entries)

    r = solve_7a(steps)
    print('The order of the steps: {}'.format(r))
