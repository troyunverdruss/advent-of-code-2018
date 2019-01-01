import sys

sys.path.append('/Users/troy/Documents/code/advent-of-code')
from y2018.d16.puzzle_16 import *
from y2018.d19.puzzle_19 import Operation


def solve_21():
    ops = {'addr': addr(), 'addi': addi(), 'mulr': mulr(), 'muli': muli(), 'banr': banr(), 'bani': bani(),
           'borr': borr(), 'bori': bori(), 'setr': setr(), 'seti': seti(), 'gtir': gtir(), 'gtri': gtri(),
           'gtrr': gtrr(), 'eqir': eqir(), 'eqri': eqri(), 'eqrr': eqrr()}

    entries = read_raw_entries(__file__, 'input.txt')

    instruction_pointer_loc = int(entries.pop(0).split()[1])

    instructions = {}
    for i in range(len(entries)):
        instructions[i] = Operation(entries[i].split())

    registers = [0, 0, 0, 0, 0, 0]

    instruction_pointer = registers[instruction_pointer_loc]
    print(registers)

    tick = 0
    first = True
    seen = {}
    last = None
    while instruction_pointer < len(instructions):
        tick += 1

        registers[instruction_pointer_loc] = instruction_pointer

        i = instructions[instruction_pointer]

        registers[instruction_pointer_loc] = instruction_pointer

        registers[i.c] = ops[i.i].do(registers, i)
        instruction_pointer = registers[instruction_pointer_loc] + 1

        reg_value = registers[5]
        if registers[instruction_pointer_loc] == 28:
            if first:
                print('Part 1: {}'.format(reg_value))
                first = False

            if reg_value in seen:
                print('Part 2: {}'.format(last))
                break

            if len(seen) % 100 == 0:
                print('Total unique entries: {}'.format(len(seen)))

            seen[reg_value] = True
            last = reg_value

    return registers[0]


if __name__ == '__main__':
    r = solve_21()
    print(r)
