from collections import deque
from helpers.helpers import read_raw_entries, path
from typing import List, Dict, Tuple
import re
import sys
from copy import deepcopy


class Pot:
    def __init__(self, value, id=None):
        self.id: int = id
        self.value: bool = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __and__(self, other):
        return self.value & other.value

    def __repr__(self):
        return repr('{}: {}'.format(self.id, self.value))

    def __bool__(self):
        return self.value

    def compute_value(self):
        if self.value:
            return self.id
        return 0

    @staticmethod
    def create_pot_from_str(id, str):
        return Pot(str_bool(str), id)


def str_bool(str):
    if str == '.':
        return False
    elif str == '#':
        return True
    else:
        raise Exception('Invalid input string: {}'.format(str))


def bool_str(bool):
    if bool:
        return '#'
    else:
        return '.'


def padleft(state: deque, count: int):
    for i in range(count):
        state.appendleft(Pot(False, state[0].id - 1))


def padright(state: deque, count: int):
    for i in range(count):
        state.append(Pot(False, state[len(state) - 1].id + 1))


def init_rules_false(rules):
    for a in [True, False]:
        for b in [True, False]:
            for c in [True, False]:
                for d in [True, False]:
                    for e in [True, False]:
                        rules[tuple([a, b, c, d, e])] = False



def process_input(entries) -> Tuple[deque, Dict[Tuple, bool]]:
    state = deque()
    rules = {}

    # init_rules_false(rules)

    # First line
    initial_state = entries.pop(0)
    initial_state = initial_state.replace('initial state: ', '')
    atoms = list(initial_state)

    for i in range(len(atoms)):
        state.append(Pot.create_pot_from_str(i, atoms[i]))

    p = re.compile(r'([.#]{5})\s+=>\s+([.#])')
    for entry in entries:
        matcher = p.match(entry)
        if matcher:
            rule = matcher.group(1)
            result = matcher.group(2)
            key = []
            for v in (list(rule)):
                key.append(str_bool(v))

            rules[tuple(key)] = str_bool(result)

    # for k, v in rules.items():
    #     print(k, v)

    return state, rules

def pad_generation(state, good=True):
    if state[0] or state[1] or state[2]:
        padleft(state, 2)
    if state[-1] or state[-2] or state[-3]:
        if good:
            padright(state, 3)
        else:
            padright(state, 2)


def run_generation(state, rules, good=True):
    pad_generation(state, good)

    new_values = {}
    for i in range(2, len(state) - 2):
        key = tuple(map(lambda x: x.value, list(state)[i - 2:i + 3]))
        if key not in rules:
            new_values[state[i].id] = False
        else:
            new_values[i] = rules[key]

    print_state(str(good)[:4], state)

    for k in new_values.keys():
        state[k].value = new_values[k]

    print_state(str(good)[:4], state)


def print_state(i, state):
    print('{}: '.format(i), end='')
    for v in state:
        if v.id == 0:
            print('|', end='')
        print(bool_str(v.value), end='')
    print('')
    sys.stdout.flush()


def solve_12(entries):
    state, rules = process_input(entries)

    print('..', end='')
    print_state(0, state)
    for i in range(110):
        run_generation(state, rules)
        if i == 19:
            print_state(i+1, state)
            get_result(state)

    print_state(110, state)

    return get_result(state)


def get_result(state):
    result = 0
    for pot in state:
        result += pot.compute_value()
    print(result)
    return result


if __name__ == '__main__':
    entries = read_raw_entries(path(__file__, 'input.txt'))
    r = solve_12(entries)
    # print(r)
    # 3738
    # 4197