def read_numeric_entries(input):
    entries = []
    with open(input, 'r', encoding='utf8') as f:
        for line in f:
            entries.append(int(line.strip()))

    return entries


def read_raw_entries(input):
    entries = []
    with open(input, 'r', encoding='utf8') as f:
        for line in f:
            entries.append(line.strip())

    return entries
