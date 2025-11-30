#!/usr/bin/env python3


ExampleInput1 = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
"""


def parse(s):
    return tuple(tuple(map(int, line.split("/"))) for line in s.splitlines())


def longest_or_strongest(con, parts, keyfn):
    if len(parts) == 0:
        return (0, 0)

    best = (0, 0)
    for i, (a, b) in enumerate(parts):
        if b == con:
            a, b = b, a
        if a == con:
            ln, st = longest_or_strongest(b, parts[:i] + parts[i+1:], keyfn)
            best = max(best, keyfn(1 + ln, a + b + st))
    return keyfn(*best)


def strongest(con, parts):
    return longest_or_strongest(con, parts, lambda ln, st: (st, ln))


def longest(con, parts):
    return longest_or_strongest(con, parts, lambda ln, st: (ln, st))


def part1(s):
    return strongest(0, parse(s))[1]


def part2(s):
    return longest(0, parse(s))[1]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (31)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (1511)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (19)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1471)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
