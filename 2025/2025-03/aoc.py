#!/usr/bin/env python3

MultiLineExample = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""

ExamplesPart1 = (
    (MultiLineExample, 357),
)

ExamplesPart2 = (
    (MultiLineExample, 3121910778619),
)


def parse(s):
    nums = []
    for line in s.splitlines():
        nums.append(list(map(int, line)))
    return nums


def best_joltage(b):
    n1 = max(b[:-1])
    i = b.index(n1)
    n2 = max(b[i+1:])
    return n1 * 10 + n2


def part1(s):
    return sum(map(best_joltage, parse(s)))


def best_joltage_recur(b, wanted, accum):
    if wanted == 0:
        return

    if wanted == len(b):
        accum += b
        return

    n = max(b[:-(wanted - 1)]) if wanted > 1 else max(b)
    i = b.index(n)
    accum.append(n)
    best_joltage_recur(b[i+1:], wanted - 1, accum)


def best_joltage2(b):
    accum = []
    best_joltage_recur(b, 12, accum)
    j = int(''.join(map(str,accum)))
    return j


def part2(s):
    return sum(map(best_joltage2, parse(s)))


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

    print("Part 1 (17430)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (171975854269367)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
