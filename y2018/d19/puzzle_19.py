from copy import deepcopy

from y2018.d16.puzzle_16 import *


class Operation:
    def __init__(self, values):
        self.i = values[0]
        self.a = int(values[1])
        self.b = int(values[2])
        self.c = int(values[3])

    def __repr__(self):
        return repr('{} {} {} {}'.format(self.i, self.a, self.b, self.c))


def solve_19(input, initial_registers=None):
    ops = {'addr': addr(), 'addi': addi(), 'mulr': mulr(), 'muli': muli(), 'banr': banr(), 'bani': bani(),
           'borr': borr(), 'bori': bori(), 'setr': setr(), 'seti': seti(), 'gtir': gtir(), 'gtri': gtri(),
           'gtrr': gtrr(), 'eqir': eqir(), 'eqri': eqri(), 'eqrr': eqrr()}

    entries = read_raw_entries(__file__, input)
    instruction_pointer_loc = int(entries.pop(0).split()[1])
    instructions = {}
    for i in range(len(entries)):
        instructions[i] = Operation(entries[i].split())

    if initial_registers:
        registers = initial_registers
    else:
        registers = [0, 0, 0, 0, 0, 0]

    instruction_pointer = registers[instruction_pointer_loc]

    initial_register_zero = registers[0]

    tick = 0
    change_count = 0
    while instruction_pointer < len(instructions):
        start_registers = deepcopy(registers)
        tick += 1
        # print(tick)
        # if tick > 100:
        #     break
        # print('IP: {}'.format(instruction_pointer))
        registers[instruction_pointer_loc] = instruction_pointer
        # print('1:      {}'.format(registers))

        i = instructions[instruction_pointer]

        registers[instruction_pointer_loc] = instruction_pointer
        # print('2:      {}'.format(registers))

        registers[i.c] = ops[i.i].do(registers, i)
        # if registers[0] != start_registers[0] or registers[5] != start_registers[5] or \
        #         registers[instruction_pointer_loc] in [6, 11]:

        # print('Before: {}'.format(registers))
        # print('{} Instruction: {}'.format(registers[instruction_pointer_loc], i))
        # print('Final:  {}'.format(registers))
        # print('')

        instruction_pointer = registers[instruction_pointer_loc] + 1


        # if registers[0] != initial_register_zero and change_count > 0:
        #     change_count += 1
        #     break
        print(registers)
# 3 5 15 21 83

    print(tick)
    return registers[0]


if __name__ == '__main__':
    # r = solve_19('input.txt')
    # print('Part 1: {}'.format(r))
    #
    r = solve_19('input.txt', [1, 0, 0, 0, 0, 0])
    print('Part 2: {}'.format(r,))
