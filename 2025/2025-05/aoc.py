#!/usr/bin/env python3

from more_itertools import ilen


MultiLineExample = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

ExamplesPart1 = (
    (MultiLineExample, 3),
)

ExamplesPart2 = (
    (MultiLineExample, 14),
)


def parse(s):
    sranges, sids = s.split("\n\n")

    ranges = []
    for rs in sranges.splitlines():
        nums = rs.split('-')
        ranges.append(range(int(nums[0]), int(nums[1])+1))

    ids = list(map(int, sids.splitlines()))
    return ranges, ids



def part1(s):
    ranges, ids = parse(s)

    return ilen(i for i in ids if any(i in r for r in ranges))


def compact(ranges):
    ranges.sort(key=lambda r: (r.start, r.stop))

    after = []
    r, ranges = ranges[0], ranges[1:]
    a, b = r.start, r.stop
    for r in ranges:
        if b >= r.start:
            b = max(b, r.stop)
        else:
            after.append(range(a, b))
            a, b, = r.start, r.stop
    after.append(range(a, b))

    return after


def part2(s):
    ranges, _ = parse(s)
    ranges = compact(ranges)
    return sum(map(len, ranges))


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

    print("Part 1 (690)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (344323629240733)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
