#!/usr/bin/env python3

import re


MultiLineExample = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""

ExamplesPart1 = (
    (MultiLineExample, 62842880),
)

ExamplesPart2 = (
    (MultiLineExample, 57600000),
)


def parse(s):
    return [[int(x) for x in re.findall(r"-?\d+", line)] for line in s.splitlines()]


def score(spec, amts):
    tscore = 1
    for prop in range(len(spec[0]) - 1):
        pscore = 0
        for i, amt in enumerate(amts):
            pscore += amt * spec[i][prop]
        tscore *= max(0, pscore)
    return tscore


def calories(spec, amts):
    return sum(amt * spec[i][-1] for i, amt in enumerate(amts))


def rcombos(nvars, total):
    if nvars == 1:
        yield [total]
        return

    for i in range(total + 1):
        for suffix in rcombos(nvars - 1, total - i):
            yield [i] + suffix


def part1(s):
    spec = parse(s)
    return max(score(spec, amts) for amts in rcombos(len(spec), 100))


def part2(s):
    spec = parse(s)
    return max(score(spec, amts) for amts in rcombos(len(spec), 100) if calories(spec, amts) == 500)


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

    print("Part 1 (13882464)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (11171160)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
