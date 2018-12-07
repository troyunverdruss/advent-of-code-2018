from helpers.helpers import read_raw_entries


def is_diff_one(a, b):
    if len(a) != len(b):
        raise Exception('Lengths not equal')

    diffs = 0
    for i in range(0, len(a)):
        if a[i] != b[i]:
            diffs += 1
            if diffs > 1:
                return False

    return diffs == 1


def diff_count(a, b):
    if len(a) != len(b):
        raise Exception('Lengths not equal')

    diffs = 0
    for i in range(0, len(a)):
        if a[i] != b[i]:
            diffs += 1

    return diffs


def get_common(a, b):
    if len(a) != len(b):
        raise Exception('Lengths not equal')

    common = ''
    for i in range(0, len(a)):
        if a[i] == b[i]:
            common += a[i]

    return common


def run_puzzle(entries):
    for i in range(0, len(entries)):
        for j in range(i+1, len(entries)):
            if is_diff_one(entries[i], entries[j]):
                return get_common(entries[i], entries[j])

    raise Exception('Could not find a single answer!')



if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    result = run_puzzle(entries)
    print('Found common letters: {}'.format(result))
