from helpers.helpers import read_raw_entries
import re
import itertools


class Sample:
    def __init__(self, before, opcode, after):
        self.before = before
        self.opcode = opcode
        self.after = after

    def __repr__(self):
        return repr('B: {}, O: {}, A: {}'.format(self.before, self.opcode, self.after))


class opcode:
    @staticmethod
    def verify_state_is_basically_ok(sample):
        for i in range(4):
            if sample.opcode[3] == i:
                continue
            if sample.before[i] != sample.after[i]:
                return False
        return True

class addr(opcode):
    @staticmethod
    def test(sample):
        # addr (add register) stores into register C the result of adding register A and register B.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] + sample.before[sample.opcode[2]] == sample.after[sample.opcode[3]]:
            return True


class addi(opcode):
    @staticmethod
    def test(sample):
        # addi (add immediate) stores into register C the result of adding register A and value B.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] + sample.opcode[2] == sample.after[sample.opcode[3]]:
            return True


class mulr(opcode):
    @staticmethod
    def test(sample):
        # mulr (multiply register) stores into register C the result of multiplying register A and register B.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] * sample.before[sample.opcode[2]] == sample.after[sample.opcode[3]]:
            return True


class muli(opcode):
    @staticmethod
    def test(sample):
        # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] * sample.opcode[2] == sample.after[sample.opcode[3]]:
            return True


class banr(opcode):
    @staticmethod
    def test(sample):
        # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] & sample.before[sample.opcode[2]] == sample.after[sample.opcode[3]]:
            return True


class bani(opcode):
    @staticmethod
    def test(sample):
        # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] & sample.opcode[2] == sample.after[sample.opcode[3]]:
            return True


class borr(opcode):
    @staticmethod
    def test(sample):
        # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] | sample.before[sample.opcode[2]] == sample.after[sample.opcode[3]]:
            return True


class bori(opcode):
    @staticmethod
    def test(sample):
        # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] | sample.opcode[2] == sample.after[sample.opcode[3]]:
            return True


class setr(opcode):
    @staticmethod
    def test(sample):
        # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.before[sample.opcode[1]] == sample.after[sample.opcode[3]]:
            return True


class seti(opcode):
    @staticmethod
    def test(sample):
        # seti (set immediate) stores value A into register C. (Input B is ignored.)
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if sample.opcode[1] == sample.after[sample.opcode[3]]:
            return True


class gtir(opcode):
    @staticmethod
    def test(sample):
        # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode[3]] and sample.opcode[1] > sample.before[sample.opcode[2]]) or \
                (0 == sample.after[sample.opcode[3]] and sample.opcode[1] <= sample.before[sample.opcode[2]]):
            return True


class gtri(opcode):
    @staticmethod
    def test(sample):
        # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode[3]] and sample.before[sample.opcode[1]] > sample.opcode[2]) or \
                (0 == sample.after[sample.opcode[3]] and sample.before[sample.opcode[1]] <= sample.opcode[2]):
            return True


class gtrr(opcode):
    @staticmethod
    def test(sample):
        # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode[3]] and sample.before[sample.opcode[1]] > sample.before[sample.opcode[2]]) or \
                (0 == sample.after[sample.opcode[3]] and sample.before[sample.opcode[1]] <= sample.before[sample.opcode[2]]):
            return True

# done vvv

class eqir(opcode):
    @staticmethod
    def test(sample):
        # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode[3]] and sample.opcode[1] == sample.before[sample.opcode[2]]) or \
                (0 == sample.after[sample.opcode[3]] and sample.opcode[1] != sample.before[sample.opcode[2]]):
            return True


class eqri(opcode):
    @staticmethod
    def test(sample):
        # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode[3]] and sample.before[sample.opcode[1]] == sample.opcode[2]) or \
                 (0 == sample.after[sample.opcode[3]] and sample.before[sample.opcode[1]] != sample.opcode[2]):
            return True


class eqrr(opcode):
    @staticmethod
    def test(sample):
        # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        if not opcode.verify_state_is_basically_ok(sample):
            return False

        if (1 == sample.after[sample.opcode[3]] and sample.before[sample.opcode[1]] == sample.before[sample.opcode[2]]) or \
                 (0 == sample.after[sample.opcode[3]] and sample.before[sample.opcode[1]] != sample.before[sample.opcode[2]]):
            return True


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


opcodes = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def find_match_count(sample, limit=3):
    matches = 0
    for op in opcodes:
        if op.test(sample):
            matches += 1
            # print('Matched: {}'.format(op))

        if matches >= limit:
            return matches

    return matches


def solve_16(samples):
    matches_three = 0
    i = 0
    print(len(samples))
    for sample in samples:
        m = find_match_count(sample, limit=16)

        print('{}: {} matches'.format(i, m))
        if m >= 3:
            matches_three += 1

        if i == 780:
            print(sample)
        i += 1

    return matches_three


if __name__ == '__main__':
    entries = read_raw_entries('input-part1.txt')
    samples = parse_samples(entries)

    count = solve_16(samples)
    print('Matches 3: {}'.format(count))

    # 547, 556
