import string
from helpers import read_raw_entries, path
import re


def solve_5a(polymer):
    atoms = list(polymer)

    modified = True
    while modified:
        modified = False
        for i, atom in enumerate(atoms):
            if i + 1 < len(atoms) and atoms[i] == atoms[i+1].swapcase():
                atoms = atoms[:i] + atoms[i + 2:]
                modified = True
                break

    return ''.join(atoms)


def solve_try_1(polymer: str):
    first = True
    regex = ''
    for l in list(string.ascii_lowercase):
        if not first:
            regex += '|'
        first = False

        c1 = l
        c2 = l.swapcase()
        regex += '{}{}|{}{}'.format(c1, c2, c2, c1)

    p = re.compile(regex)

    modified = True
    while modified:
        new_polymer = re.sub(p, '', polymer)
        modified = new_polymer != polymer
        polymer = new_polymer

    return polymer

def solve_5b(polymer):
    letters = list(string.ascii_lowercase)

    shortest_polymer = len(polymer) * 2

    for letter in letters:
        print(letter)
        stripped = re.sub(r'[{}{}]'.format(letter, letter.swapcase()), '', polymer)
        print('{} stripped length: {}'.format(letter, len(stripped)))
        compressed_polymer_length = len(solve_try_1(stripped))
        if (compressed_polymer_length) < shortest_polymer:
            shortest_polymer = compressed_polymer_length

    return shortest_polymer

if __name__ == '__main__':
    polymer = read_raw_entries(path(__file__, 'input.txt'))[0]
    result = solve_try_1(polymer)
    print('Compressed polymer length: {}'.format(len(result)))

    polymer = read_raw_entries(path(__file__, 'input.txt'))[0]
    result = solve_5b(polymer)
    print('Shortest possible compressed polymer length: {}'.format(result))
