#!/usr/bin/env pypy3

ExampleInput1 = """\
5-8
0-2
4-7
"""


def parse(s):
    return [tuple(map(int, line.split("-"))) for line in s.splitlines()]


def find_allowed(s, first=False):
    ranges = parse(s)
    ranges.sort()
    stop = 0
    count = 0
    for a, b in ranges:
        if (delta := a - stop) > 0:
            if first:
                return stop
            count += delta
        stop = max(stop, b + 1)

    count += 2**32 - stop
    return count


def part1(s):
    return find_allowed(s, first=True)


def part2(s):
    return find_allowed(s, first=False)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (3)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (31053880)")
    print(part1(real_input()))

    print()
    print("Part 2 (117)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
