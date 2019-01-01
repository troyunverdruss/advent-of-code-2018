from helpers.helpers import read_raw_entries
import re
import itertools


class Sample:
    def __init__(self, before, opcode, after):
        self.before = before
        self.opcode = Operation(opcode)
        self.after = after

    def __repr__(self):
        return repr('B: {}, O: {}, A: {}'.format(self.before, self.opcode, self.after))


class Operation:
    def __init__(self, values):
        self.i = int(values[0])
        self.a = int(values[1])
        self.b = int(values[2])
        self.c = int(values[3])


class opcode:
    def __init__(self):
        self.matches = {}
        self.opcode = None

    def verify_state_is_basically_ok(self, sample):
        for i in range(4):
            if sample.opcode.c == i:
                continue
            if sample.before[i] != sample.after[i]:
                return False
        return True

    def register_match(self, sample):
        if sample.opcode.i not in self.matches:
            self.matches[sample.opcode.i] = 1
        else:
            self.matches[sample.opcode.i] += 1
        return True


class addr(opcode):

    def test(self, sample):
        # addr (add register) stores into register C the result of adding register A and register B.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] + sample.before[sample.opcode.b] == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a] + register[opcode.b]


class addi(opcode):

    def test(self, sample):
        # addi (add immediate) stores into register C the result of adding register A and value B.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] + sample.opcode.b == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a] + opcode.b


class mulr(opcode):

    def test(self, sample):
        # mulr (multiply register) stores into register C the result of multiplying register A and register B.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] * sample.before[sample.opcode.b] == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a] * register[opcode.b]


class muli(opcode):

    def test(self, sample):
        # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] * sample.opcode.b == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a] * opcode.b


class banr(opcode):

    def test(self, sample):
        # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] & sample.before[sample.opcode.b] == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a] & register[opcode.b]


class bani(opcode):

    def test(self, sample):
        # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] & sample.opcode.b == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a] & opcode.b


class borr(opcode):

    def test(self, sample):
        # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] | sample.before[sample.opcode.b] == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a] | register[opcode.b]


class bori(opcode):

    def test(self, sample):
        # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] | sample.opcode.b == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a] | opcode.b


class setr(opcode):

    def test(self, sample):
        # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode.a] == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return register[opcode.a]


class seti(opcode):

    def test(self, sample):
        # seti (set immediate) stores value A into register C. (Input B is ignored.)
        if not super().verify_state_is_basically_ok(sample):
            return False

        if sample.opcode.a == sample.after[sample.opcode.c]:
            return super().register_match(sample)

    def do(self, register, opcode):
        return opcode.a


class gtir(opcode):

    def test(self, sample):
        # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode.c] and sample.opcode.a > sample.before[sample.opcode.b]) or \
                (0 == sample.after[sample.opcode.c] and sample.opcode.a <= sample.before[sample.opcode.b]):
            return super().register_match(sample)

    def do(self, register, opcode):
        if opcode.a > register[opcode.b]:
            return 1
        else:
            return 0


class gtri(opcode):

    def test(self, sample):
        # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode.c] and sample.before[sample.opcode.a] > sample.opcode.b) or \
                (0 == sample.after[sample.opcode.c] and sample.before[sample.opcode.a] <= sample.opcode.b):
            return super().register_match(sample)

    def do(self, register, opcode):
        if register[opcode.a] > opcode.b:
            return 1
        else:
            return 0


class gtrr(opcode):

    def test(self, sample):
        # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode.c] and sample.before[sample.opcode.a] > sample.before[
            sample.opcode.b]) or \
                (0 == sample.after[sample.opcode.c] and sample.before[sample.opcode.a] <= sample.before[
                    sample.opcode.b]):
            return super().register_match(sample)

    def do(self, register, opcode):
        if register[opcode.a] > register[opcode.b]:
            return 1
        else:
            return 0


# done vvv

class eqir(opcode):

    def test(self, sample):
        # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode.c] and sample.opcode.a == sample.before[sample.opcode.b]) or \
                (0 == sample.after[sample.opcode.c] and sample.opcode.a != sample.before[sample.opcode.b]):
            return super().register_match(sample)

    def do(self, register, opcode):
        if opcode.a == register[opcode.b]:
            return 1
        else:
            return 0


class eqri(opcode):

    def test(self, sample):
        # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode.c] and sample.before[sample.opcode.a] == sample.opcode.b) or \
                (0 == sample.after[sample.opcode.c] and sample.before[sample.opcode.a] != sample.opcode.b):
            return super().register_match(sample)

    def do(self, register, opcode):
        if register[opcode.a] == opcode.b:
            return 1
        else:
            return 0


class eqrr(opcode):

    def test(self, sample):
        # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        if not super().verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode.c] and sample.before[sample.opcode.a] == sample.before[
            sample.opcode.b]) or \
                (0 == sample.after[sample.opcode.c] and sample.before[sample.opcode.a] != sample.before[
                    sample.opcode.b]):
            return super().register_match(sample)

    def do(self, register, opcode):
        if register[opcode.a] == register[opcode.b]:
            return 1
        else:
            return 0


def parse_samples(entries):
    i = 0

    b = re.compile(r'Before: \[(\d), (\d), (\d), (\d)\]')
    o = re.compile(r'(\d+) (\d) (\d) (\d)')
    a = re.compile(r'After:  \[(\d), (\d), (\d), (\d)]')

    samples = []
    before, opcode, after = None, None, None
    for line in entries:
        # print(line)
        if i % 4 == 0:
            m = b.match(line)
            before = tuple([int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))])
        elif i % 4 == 1:
            m = o.match(line)
            opcode = tuple([int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))])
        elif i % 4 == 2:
            m = a.match(line)
            after = tuple([int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))])
        elif i % 4 == 3:
            samples.append(Sample(before, opcode, after))
            before, opcode, after = None, None, None
        i += 1

    return samples


def find_match_count(sample, opcodes, limit=3):
    matches = 0
    for op in opcodes:
        if op.test(sample):
            matches += 1
            # print('Matched: {}'.format(op))

        if matches >= limit:
            return matches

    return matches


def solve_16(samples, opcodes):
    matches_three = 0
    i = 0
    # print(len(samples))
    for sample in samples:
        m = find_match_count(sample, opcodes, limit=16)

        # print('{}: {} matches'.format(i, m))
        if m >= 3:
            matches_three += 1

        i += 1

    return matches_three


def remove_matched_codes(to_remove, opcodes):
    for o in opcodes:
        for tr in to_remove:
            o.matches.pop(tr, None)


def solve_opcodes(opcodes):
    codes = list(range(16))
    to_remove = []

    while codes:
        remove_matched_codes(to_remove, opcodes)

        sorted_codes = list(sorted(filter(lambda o: len(o.matches.keys()) > 0, opcodes), key=lambda o: len(o.matches)))
        first = sorted_codes[0]
        if len(first.matches) == 1:
            codes.remove(list(first.matches.keys())[0])
            first.opcode = list(first.matches.keys())[0]
            to_remove.append(list(first.matches.keys())[0])



def solve_16_part_2(entries, opcodes):
    instructions = []
    for entry in entries:
        instructions.append(entry.split())

    opcode_lookup = {}
    for o in opcodes:
        opcode_lookup[o.opcode] = o

    for k in sorted(opcode_lookup.keys()):
        print('{}: {}'.format(k, opcode_lookup[k]))

    register = [0,0,0,0] #[int(instructions[0][0]), int(instructions[0][1]), int(instructions[0][2]), int(instructions[0][3])]
    i = 0
    for instruction in instructions:
        print('{} Running instruction: {}'.format(i, instruction), end='')
        operation = Operation(instruction)
        register[operation.c] = opcode_lookup[operation.i].do(register, operation)
        print(' = {}'.format(register))
        i += 1

    return register[0]


if __name__ == '__main__':
    entries = read_raw_entries(__file__, 'input-part1.txt')
    samples = parse_samples(entries)

    opcodes = [addr(), addi(), mulr(), muli(), banr(), bani(), borr(), bori(), setr(), seti(), gtir(), gtri(), gtrr(),
               eqir(), eqri(), eqrr()]

    count = solve_16(samples, opcodes)
    print('Matches 3: {}'.format(count))

    solve_opcodes(opcodes)

    # 547, 556, 542

    entries = read_raw_entries(__file__, "input-part2.txt")
    r = solve_16_part_2(entries, opcodes)
    print('Result: {}'.format(r))
