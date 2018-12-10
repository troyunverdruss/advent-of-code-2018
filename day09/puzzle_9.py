from helpers.helpers import read_raw_entries
from typing import List, Dict, Tuple
import re


class Marble:
    def __init__(self, prev=None, next=None, value=None):
        self.prev = prev
        self.next = next
        self.value = value

    def __repr__(self):
        return repr(self.value)


class Circle:
    def __init__(self):
        self.active_marble = Marble(value=0)
        self.active_marble.prev = self.active_marble
        self.active_marble.next = self.active_marble

    def add_marble(self, marble_value: int, compute_board_str=False) -> Tuple[int, str]:
        score = 0
        if marble_value % 23 == 0:
            score += marble_value

            for i in range(0, 7):
                self.active_marble = self.active_marble.prev

            score += self.active_marble.value
            self.active_marble.prev.next = self.active_marble.next
            self.active_marble.next.prev = self.active_marble.prev
            self.active_marble = self.active_marble.next

        else:
            self.active_marble = self.active_marble.next

            new_marble = Marble(prev=self.active_marble, next=self.active_marble.next, value=marble_value)
            self.active_marble.next.prev = new_marble
            self.active_marble.next = new_marble
            self.active_marble = new_marble

        # This is an optional view of the board, mostly for debugging
        string_version_of_board = ''
        if compute_board_str:
            string_version_of_board = '({}) '.format(self.active_marble.value)
            curr = self.active_marble
            while curr.next != self.active_marble:
                curr = curr.next
                string_version_of_board += '{} '.format(curr.value)

        return score, string_version_of_board


def parse_params(input: str) -> Tuple[int, int]:
    p = re.compile(r'(\d+) players; last marble is worth (\d+) points')
    matcher = p.match(input)

    if not matcher:
        raise Exception('Could not parse input string')

    return int(matcher.group(1)), int(matcher.group(2))


def solve_9(input: str, multiplier: int = 1):
    player_count, last_marble_value = parse_params(input)
    last_marble_value *= multiplier

    scores: List[int] = []
    for i in range(0, player_count):
        scores.append(0)

    circle = Circle()

    marble_value = 1
    while marble_value <= last_marble_value:
        score, string_rep = circle.add_marble(marble_value)
        scores[(marble_value - 1) % player_count] += score
        marble_value += 1

    return max(scores)


if __name__ == '__main__':
    input = read_raw_entries('input.txt')[0].strip()
    r = solve_9(input, 1)
    print('9a. Winning score: {}'.format(r))

    input = read_raw_entries('input.txt')[0].strip()
    r = solve_9(input, 100)
    print('9b. Winning score: {}'.format(r))
