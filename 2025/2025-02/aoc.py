#!/usr/bin/env python3

MultiLineExample = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""

ExamplesPart1 = (
    (MultiLineExample, 1227775554),
)

ExamplesPart2 = (
    (MultiLineExample, 4174379265),
)


def parse(s):
    ranges = []
    for rs in s.split(","):
        nums = rs.split('-')
        ranges.append(range(int(nums[0]), int(nums[1])+1))
    return ranges


def valid1(n):
    ns = str(n)
    if len(ns) % 2 == 0:
        if ns[:len(ns)//2] == ns[len(ns)//2:]:
            return False
    return True


def sum_invalid(ranges, validfn):
    total = 0
    for r in ranges:
        for n in r:
            if not validfn(n):
                total += n
    return total


def part1(s):
    return sum_invalid(parse(s), valid1)


def valid2(n):
    ns = str(n)
    for x in range(1,len(ns)//2 + 1):
        if len(ns) % x == 0:
            rpt = len(ns) // x
            if ns == (ns[:x] * rpt):
                return False
    return True


def part2(s):
    return sum_invalid(parse(s), valid2)


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

    print("Part 1 (15873079081)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (22617871034)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
