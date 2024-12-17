#!/usr/bin/env pypy3

ExampleInput1 = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

ExampleInput2 = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

# combo operands:
# 0 1 2 3 - literal
# 4 5 6 - register A B C
# 7 - undefined

ops = [
    'adv', # DIV: A / 2**combo (trunc int) -> A
    'bxl', # OR: B | literal -> B
    'bst', # MOD8: combo % 8 -> B
    'jnz', # A == 0 ? NOOP : jmp(literal) [ip does not advance]
    'bxc', # XOR: B ^ C -> B [operand ignored]
    'out', # combo % 8 -> output
    'bdv', # DIV: A / 2**combo (trunc int) -> B
    'cdv', # DIV: A / 2**combo (trunc int) -> C
    # HALT when ip is outside program
]


class Computer:
    def __init__(self, a, b, c, prog):
        self.a = a
        self.b = b
        self.c = c
        self.prog = prog
        self.ip = 0
        self.output = []

    def __repr__(self):
        return f"Computer: a={self.a} b={self.b} c={self.c} output={self.output}"

    def run(self):
        while self.ip in range(len(self.prog) - 1):
            self.run_one()

    def combo(self, operand):
        match operand:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case n:
                return n

    def run_one(self):
        opcode, operand, *_ = self.prog[self.ip:]

        match ops[opcode]:
            case 'adv':
                self.a = int(self.a / 2**self.combo(operand))

            case 'bxl':
                self.b = self.b ^ operand

            case 'bst':
                self.b = self.combo(operand) % 8

            case 'jnz':
                if self.a != 0:
                    self.ip = operand
                    return

            case 'bxc':
                self.b = self.b ^ self.c

            case 'out':
                self.output.append(self.combo(operand) % 8)

            case 'bdv':
                self.b = int(self.a / 2**self.combo(operand))

            case 'cdv':
                self.c = int(self.a / 2**self.combo(operand))

        self.ip += 2

    def calc(self, a):
        self.ip = 0
        self.a = a
        self.b = 0
        self.c = 0
        self.output = []
        self.run()
        return self.output


def parse(s):
    s = s.splitlines()
    a = int(s[0].split(': ')[1])
    b = int(s[1].split(': ')[1])
    c = int(s[2].split(': ')[1])
    prog = list(map(int, s[4].split(': ')[1].split(',')))
    return Computer(a, b, c, prog)

def part1(s):
    c = parse(s)
    c.run()
    return ",".join(map(str, c.output))


# Manual steps I took:
#
#  1. Found the (lowest) range of inputs that gave an output of the correct
#     length: range(2**45, 2**48)
#
#  2. Noticed that 48 is divisble by 3 and everything about the problem clues
#     octal values pretty hard. So the input is a 16-digit octal value. JUST
#     LIKE THE DESIRED OUTPUT.
#
#  3. Messed around with some inputs and noticed that leftmost bits in the
#     input effect rightmost bits in the output.
#
#  So I think a brute force stategy that could work is construct a 16-digit
#  octal input, and DFS when the nth leftmost digit gives the correct nth
#  rightmost digit.
def part2(s):
    c = parse(s)
    proglen = len(c.prog)

    def seq2int(seq):
        seq = seq + [0] * (proglen - len(seq))
        return int("".join(map(str, seq)), 8)
    def correctness(out):
        for i in range(len(out)):
            try:
                if out[-i-1] != c.prog[-i-1]:
                    return i
            except IndexError:
                return i
        return len(out)
    def search(inseq):
        depth = len(inseq)
        for n in range(8):
            seq = inseq + [n]
            a = seq2int(seq)
            out = c.calc(a)
            correct = correctness(out)
            #print(f"{depth} {n} {a:016o} {out} {correct}")
            if correct == len(c.prog):
                return a
            if correct > depth:
                found = search(seq)
                if found:
                    return found
        return None

    return search([])


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (4,6,3,5,6,3,5,2,1,0)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (6,1,6,4,2,4,7,3,5)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (117440)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (202975183645226)")
    print(part2(real_input()))



if __name__ == "__main__":
    run_all()
