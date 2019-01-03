from helpers import read_raw_entries


def solve_2a(entries):
    checksum = 0

    for entry in entries:
        numbers = list(map(int, entry.split()))
        checksum += max(numbers) - min(numbers)

    return checksum


def solve_2b(entries):
    checksum = 0

    for entry in entries:
        numbers = list(map(int, entry.split()))
        for d1 in numbers:
            for d2 in numbers:
                if d1 == d2:
                    continue
                if d1 % d2 == 0:
                    checksum += d1 / d2

    return checksum


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    r = solve_2a(entries)
    print(r)

    r = solve_2b(entries)
    print(r)
