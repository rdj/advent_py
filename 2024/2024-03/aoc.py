#!/usr/bin/env python3

import re
from colors import color


ExampleInput1 = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

ExampleInput2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

def find_pairs(s):
    return ((int(a), int(b)) for a, b in re.findall(r'mul\((\d+),(\d+)\)', s))


def part1(s):
    pairs = find_pairs(s)
    return sum(a * b for a, b in pairs)


def part2(s):
    s = s + "do()"
    s = re.sub(r"(?s:don't\(\).*?do\(\))", "", s)
    return part1(s)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (161)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (167090022)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (48)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (89823704)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
