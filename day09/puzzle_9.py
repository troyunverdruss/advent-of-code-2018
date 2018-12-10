from helpers.helpers import read_raw_entries
from typing import List, Dict, Tuple
import re
import sys


class Circle:
    def __init__(self):
        self.active_marble: int = 0
        self.circle: List[int] = [0]

    def add_marble(self, marble_value: int) -> Tuple[int, str]:
        score = 0
        if marble_value % 23 == 0:
            score += marble_value

            marble_to_remove = (self.active_marble - 7) % len(self.circle)
            score += self.circle.pop(marble_to_remove)
            self.active_marble = marble_to_remove
        else:
            if len(self.circle) == 1:
                self.circle.append(marble_value)
                self.active_marble = 1
            else:
                insert_index = (self.active_marble + 1) % len(self.circle) + 1
                self.circle.insert(insert_index, marble_value)
                self.active_marble = insert_index

        # string_version_of_board = ''
        # for i in range(0, len(self.circle)):
        #     if i == self.active_marble:
        #         string_version_of_board += '({}) '.format(self.circle[i])
        #         # print('({}) '.format(self.circle[i]), end='')
        #     else:
        #         string_version_of_board += '{} '.format(self.circle[i])
        #         # print('{} '.format(self.circle[i]), end='')
        # print('')
        # sys.stdout.flush()

        return score, None


def parse_params(input: str) -> Tuple[int, int]:
    p = re.compile(r'(\d+) players; last marble is worth (\d+) points')
    matcher = p.match(input)

    if not matcher:
        raise Exception('Could not parse input string')

    return int(matcher.group(1)), int(matcher.group(2))


def solve_9a(input: str):
    player_count, last_marble_value = parse_params(input)

    scores: List[int] = []
    for i in range(0, player_count):
        scores.append(0)

    circle = Circle()

    marble_value = 1

    while marble_value <= last_marble_value:
        # print('Player number: {}, index: {}'.format((marble_value - 1) % player_count + 1,
        #                                             (marble_value - 1) % player_count))

        score, string_rep = circle.add_marble(marble_value)

        scores[(marble_value - 1) % player_count] += score

        marble_value += 1

    return max(scores)


if __name__ == '__main__':
    input = read_raw_entries('input.txt')[0].strip()
    r = solve_9a(input)
    print('Winning score: {}'.format(r))
