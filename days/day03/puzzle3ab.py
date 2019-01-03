import re
from helpers.helpers import read_raw_entries, path


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


def add_reservation(cloth, id, left, top):
    if left in cloth:
        if top in cloth[left]:
            cloth[left][top] = True
        else:
            cloth[left][top] = id
    else:
        cloth[left] = {}
        cloth[left][top] = id


def setup_cloth(claims):
    cloth = {}
    for c in claims:
        for left in range(c.left, c.left + c.width):
            for top in range(c.top, c.top + c.height):
                add_reservation(cloth, c.id, left, top)
    return cloth


def find_overlapping_square_inches(raw_entries):
    claims = parse_entries(raw_entries)
    cloth = setup_cloth(claims)

    overlapping = 0
    for x in cloth.keys():
        for y in cloth[x].keys():
            if isinstance(cloth[x][y], bool) and cloth[x][y]:
                overlapping += 1

    return overlapping


def find_intact_claim(raw_entries):
    claims = parse_entries(raw_entries)
    cloth = setup_cloth(claims)

    id_without_overlap = None

    for c in claims:
        did_overlap = False

        for left in range(c.left, c.left + c.width):
            for top in range(c.top, c.top + c.height):
                if cloth[left][top] != c.id:
                    did_overlap = True
                    break

        if not did_overlap:
            id_without_overlap = c.id

    return id_without_overlap


if __name__ == '__main__':
    entries = read_raw_entries(path(__file__, 'input.txt'))
    overlapping_square_inches = find_overlapping_square_inches(entries)
    print('3a: Found overlapping square inches: {}'.format(overlapping_square_inches))

    id_without_overlap = find_intact_claim(entries)
    print('3b: Found intact claim: {}'.format(id_without_overlap))
