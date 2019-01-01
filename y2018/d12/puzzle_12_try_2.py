from collections import deque
from helpers.helpers import read_raw_entries
from typing import List, Dict, Tuple
import re
import sys


class Pot:
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __repr__(self):
        return repr('{}: {}'.format(self.id, self.value))

    def __str__(self):
        return self.value


def padleft(state, count):
    for i in range(count):
        state.insert(0, Pot(state[0].id - 1, '.'))


def padright(state: deque, count: int):
    for i in range(count):
        state.append(Pot(state[len(state) - 1].id + 1, '.'))


def solve_12(entries, generations_to_run=20):
    pots = []
    i = 0
    entries[0] = entries[0].replace('initial state: ', '')
    for p in list(entries[0].strip()):
        pots.append(Pot(i, p))
        i += 1

    rules = {}
    p = re.compile(r'(.*)=>(.*)')
    for entry in entries:
        m = p.match(entry)
        if m:
            rules[m.group(1).strip()] = m.group(2).strip()

    last_sum = 0
    for i in range(generations_to_run):
        if '#' in map(lambda p: p.value, pots[:3]):
            padleft(pots, 2)
        if '#' in map(lambda p: p.value, pots[:-3]):
            padright(pots, 3)
        next = {}
        for j in range(2, len(pots) - 2):
            group = pots[j - 2:j + 3]
            k = ''
            for g in group:
                k += g.value
            if k not in rules:
                next[j] = '.'
            else:
                next[j] = rules[k]

        for j in next.keys():
            pots[j].value = next[j]

        sum = 0
        for p in pots:
            if p.value == '#':
                sum += p.id

        print('gen: {} sum: {}, last sum: {}, diff: {}'.format(i + 1, sum, last_sum, sum - last_sum))
        last_sum = sum

    return sum


if __name__ == '__main__':
    entries = read_raw_entries(__file__, 'input.txt')
    r = solve_12(entries)
    print(r)

    r = solve_12(entries, 200)
    print(r)

    # Correct answers
    # Gen 20 sum: 3738
    # Gen 110 sum: 11047
