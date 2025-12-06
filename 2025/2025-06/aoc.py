#!/usr/bin/env python3

from functools import reduce
import operator
import re

# Leading and trailing whitespace is important
MultiLineExample = "123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  \n"

ExamplesPart1 = (
    (MultiLineExample, 4277556),
)

ExamplesPart2 = (
    (MultiLineExample, 3263827),
)

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
}


def parse(s):
    lines = s.splitlines()
    lines = map(lambda line: line.split(), lines)
    flipped = [list(x) for x in zip(*lines)]

    probs = []
    for line in flipped:
        probs.append([OPS[line[-1]], list(map(int, line[:-1]))])

    return probs


def evalprob(p):
    op, nums = p
    return reduce(op, nums)


def part1(s):
    return sum(map(evalprob, parse(s)))


def parse2_vertically(s):
    lines = s.splitlines()

    lines, opline = lines[:-1], lines[-1]
    ops = [OPS[s] for s in opline.split()]

    w = len(lines[0])
    h = len(lines)

    assert(all(len(line) == w) for line in lines)

    probs = []
    cur = []

    for j in range(w - 1, -1, -1):
        try:
            cur.append(int("".join([lines[i][j] for i in range(h)])))
        except ValueError:
            probs.append([ops.pop(), cur])
            cur = []
    if cur:
        probs.append([ops.pop(), cur])
    assert(0 == len(ops))
    return probs


def parse2_transposed(s):
    lines = s.splitlines()
    assert(all(len(line) == len(lines[0])) for line in lines)

    lines, opline = lines[:-1], lines[-1]
    ops = [OPS[s] for s in opline.split()]

    flipped = "\n".join("".join(x) for x in zip(*lines))
    sprobs = re.split(r'^[ ]+\n', flipped, flags=re.MULTILINE)
    probs = []
    for sprob in sprobs:
        op, ops = ops[0], ops[1:]
        nums = list(map(int, sprob.splitlines()))
        probs.append([op, nums])

    assert(0 == len(ops))
    return probs


def part2(s):
    return sum(map(evalprob, parse2_transposed(s)))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (5227286044585)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 ()")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
