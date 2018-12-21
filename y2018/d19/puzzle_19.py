from y2018.d16.puzzle_16 import *


class Operation:
    def __init__(self, values):
        self.i = values[0]
        self.a = int(values[1])
        self.b = int(values[2])
        self.c = int(values[3])

    def __repr__(self):
        return repr('{} {} {} {}'.format(self.i, self.a, self.b, self.c))


def solve_19(input):
    ops = {'addr': addr(), 'addi': addi(), 'mulr': mulr(), 'muli': muli(), 'banr': banr(), 'bani': bani(),
           'borr': borr(), 'bori': bori(), 'setr': setr(), 'seti': seti(), 'gtir': gtir(), 'gtri': gtri(),
           'gtrr': gtrr(), 'eqir': eqir(), 'eqri': eqri(), 'eqrr': eqrr()}

    entries = read_raw_entries(input)
    instruction_pointer_loc = int(entries.pop(0).split()[1])
    instructions = {}
    for i in range(len(entries)):
        instructions[i] = Operation(entries[i].split())

    registers = [0, 0, 0, 0, 0, 0]

    instruction_pointer = registers[instruction_pointer_loc]

    tick = 0
    while instruction_pointer < len(instructions):
        tick += 1
        # print(tick)
        # if tick > 100:
        #     break
        # print('IP: {}'.format(instruction_pointer))
        # print('Before: {}'.format(registers))
        registers[instruction_pointer_loc] = instruction_pointer
        # print('1:      {}'.format(registers))

        i = instructions[instruction_pointer]
        # print('Instruction: {}'.format(i))

        registers[instruction_pointer_loc] = instruction_pointer
        # print('2:      {}'.format(registers))

        registers[i.c] = ops[i.i].do(registers, i)
        # print('Final:  {}'.format(registers))

        instruction_pointer = registers[instruction_pointer_loc] + 1
        # print('')

    return registers[0]


if __name__ == '__main__':
    r = solve_19('input.txt')
    print(r)
