from helpers.helpers import read_raw_entries


class Analysis:
    def __init__(self):
        self.pairs = 0
        self.triplets = 0

    def has_pairs(self):
        return self.pairs > 0

    def has_triplets(self):
        return self.triplets > 0


def analyze(entry):
    counts = {}
    for v in list(entry):
        if v in counts:
            counts[v] += 1
        else:
            counts[v] = 1

    a = Analysis()
    for k, v in counts.items():
        if v == 2:
            a.pairs += 1
        elif v == 3:
            a.triplets += 1

    return a


def run_puzzle(entries):
    total_pairs = 0
    total_triplets = 0

    for e in entries:
        analysis = analyze(e)
        if analysis.has_pairs():
            total_pairs += 1
        if analysis.has_triplets():
            total_triplets += 1

    return total_pairs * total_triplets


if __name__ == '__main__':
    entries = read_raw_entries(__file__, 'input.txt')
    result = run_puzzle(entries)
    print('Found checksum: {}'.format(result))
