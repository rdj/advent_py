#!/usr/bin/env python3

ExampleInput1 = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

ExampleInput2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def part1(s):
    a = [[int(_) for _ in line if _.isdigit()] for line in s.splitlines()]
    a = [_[0] * 10 + _[-1] for _ in a]
    return sum(a)


DIGITS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def leftmost(s):
    if s[0].isdigit():
        return int(s[0])
    for d, name in enumerate(DIGITS):
        if s.startswith(name):
            return d
    return leftmost(s[1:])


def rightmost(s):
    if s[-1].isdigit():
        return int(s[-1])
    for d, name in enumerate(DIGITS):
        if s.endswith(name):
            return d
    return rightmost(s[:-1])


def extract_part2(s):
    return leftmost(s) * 10 + rightmost(s)


def part2(s):
    a = [extract_part2(_) for _ in s.splitlines()]
    return sum(a)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (142)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (56042)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (281)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (55358)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
