from helpers.helpers import read_numeric_entries


class CurrentFreq:
    def __init__(self):
        self.value = 0


def find_dupe(freqs, current_freq, entry):
    # print('entry: {}'.format(entry))
    current_freq.value += entry
    # print('current_freq: {}'.format(current_freq.value))
    if current_freq.value in freqs:
        # print('Found duplicate freq: {}'.format(current_freq.value))
        return current_freq.value
    else:
        freqs[current_freq.value] = True
        # print(freqs)

    return None


def run_puzzle(input):
    entries = read_numeric_entries(__file__, input)

    freqs = {0: True}
    current_freq = CurrentFreq()

    result = None
    i = 0
    while result is None:
        result = find_dupe(freqs, current_freq, entries[i])
        if i + 1 == len(entries):
            i = 0
        else:
            i += 1

    return result


if __name__ == '__main__':
    result = run_puzzle('input.txt')
    print('Found duplicate frequency: {}'.format(result))
