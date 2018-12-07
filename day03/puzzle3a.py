import re
from helpers.helpers import read_raw_entries


class Claim:
    def __init__(self):
        self.id = None
        self.left = None
        self.top = None
        self.width = None
        self.height = None

    def parse(self, s):
        p = re.compile('^#(\d+)\s+@\s+(\d+),(\d+):\s+(\d+)x(\d+)$')
        matcher = p.match(s)

        if matcher:
            self.id = int(matcher.group(1))
            self.left = int(matcher.group(2))
            self.top = int(matcher.group(3))
            self.width = int(matcher.group(4))
            self.height = int(matcher.group(5))
        else:
            raise Exception('Unable to parse entry: {}'.format(s))


def parse_entries(raw_entries):
    claims = []
    for e in raw_entries:
        c = Claim()
        c.parse(e.strip())
        claims.append(c)

    return claims


def add_reservation(cloth, left, top):
    if left in cloth:
        if top in cloth[left]:
            cloth[left][top] = True
        else:
            cloth[left][top] = False
    else:
        cloth[left] = {}
        cloth[left][top] = False


def run_puzzle(raw_entries):
    claims = parse_entries(raw_entries)

    cloth = {}
    overlapping = 0

    for c in claims:
        for left in range(c.left, c.left + c.width):
            for top in range(c.top, c.top + c.height):
                add_reservation(cloth, left, top)

    for x in cloth.keys():
        for y in cloth[x].keys():
            if cloth[x][y]:
                overlapping += 1

    return overlapping


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    result = run_puzzle(entries)
    print('Found overlapping square inches: {}'.format(result))
