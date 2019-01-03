from helpers import read_raw_entries
from collections import deque


def solve_1(input, offset=1):
    d = deque(list(input))

    total = 0

    for i in range(0, len(d)):
        if d[0] == d[offset]:
            total += int(d[0])
        d.rotate(-1)
    return total


if __name__ == '__main__':
    input = read_raw_entries('input.txt')[0].strip()
    r = solve_1(input)
    print(r)

    r = solve_1(input, int(len(list(input)) / 2))
    print(r)
