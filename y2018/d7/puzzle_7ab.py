from helpers.helpers import read_raw_entries
from typing import List, Dict
import re
import string


class Step:
    def __init__(self, id, duration):
        self.id = id
        self.prereqs = []
        self.duration = duration
        self.time_remaining = duration


class Worker:
    def __init__(self):
        self.step = None

    def work(self):
        if self.step is not None:
            self.step.time_remaining -= 1

    def is_finished(self) -> bool:
        return self.step is not None and self.step.time_remaining == 0

    def can_accept_work(self) -> bool:
        return self.step is None


def compute_duration(letter: str, base_duration: int):
    return list(string.ascii_uppercase).index(letter) + 1 + base_duration


def process_into_steps(entries: List[str], base_duration: int):
    steps = {}

    p = re.compile(r'^Step (\w) must be finished before step (\w) can begin.$')

    for entry in entries:
        matcher = p.match(entry.strip())

        if not matcher:
            raise Exception('Entry could not be parsed! {}'.format(entry))

        if matcher.group(1) not in steps:
            duration = compute_duration(matcher.group(1), base_duration)
            steps[matcher.group(1)] = Step(matcher.group(1), duration)

        if matcher.group(2) not in steps:
            duration = compute_duration(matcher.group(2), base_duration)
            steps[matcher.group(2)] = Step(matcher.group(2), duration)

        steps[matcher.group(2)].prereqs.append(matcher.group(1))

    return steps


def solve_7a(steps: Dict[str, Step]) -> str:
    pending_steps = sorted(steps)
    finished_steps = []

    while len(pending_steps) > 0:
        for step in pending_steps:
            if all(s in finished_steps for s in steps[step].prereqs):
                pending_steps.remove(step)
                finished_steps.append(step)
                break

    return ''.join(finished_steps)


def get_work(steps, pending_steps, finished_steps) -> Step:
    for step in pending_steps:
        if all(s in finished_steps for s in steps[step].prereqs):
            pending_steps.remove(step)
            return steps[step]

    return None


def solve_7b(steps: Dict[str, Step], worker_count: int) -> int:
    step_count = len(steps)
    pending_steps = sorted(steps)
    finished_steps = []

    time = 0

    workers = []
    for i in range(0, worker_count):
        workers.append(Worker())

    while len(finished_steps) < step_count:
        time += 1

        # Dole out work
        for worker in workers:
            if worker.can_accept_work():
                work = get_work(steps, pending_steps, finished_steps)
                if work is None:
                    break
                worker.step = work

        for worker in workers:
            # Do work
            worker.work()

            # Clean up completed work
            if worker.is_finished():
                finished_steps.append(worker.step.id)
                worker.step = None

    return time


if __name__ == '__main__':
    entries = read_raw_entries(__file__, 'input.txt')
    steps = process_into_steps(entries, 0)

    r = solve_7a(steps)
    print('The order of the steps: {}'.format(r))

    entries = read_raw_entries(__file__, 'input.txt')
    steps = process_into_steps(entries, 60)

    r = solve_7b(steps, 5)
    print('The duration of the steps: {}'.format(r))
