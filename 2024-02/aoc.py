#!/usr/bin/env python3

from more_itertools import sliding_window


ExampleInput1 = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

def parse(s):
    return [[int(_) for _ in line.split()] for line in s.splitlines()]

def is_good(nums):
    d = [w[0] - w[1] for w in sliding_window(nums, 2)]

    if d[0] == 0:
        return False
    sign = d[0] // abs(d[0])

    norm = [_*sign for _ in d]
    return all(1 <= _ <= 3 for _ in norm)


def part1(s):
    return len([_ for _ in parse(s) if is_good(_)])


def any_good(nums):
    return is_good(nums) or any(is_good(_) for _ in [nums[:i] + nums[i+1:] for i in range(len(nums))])


def part2(s):
    return len([_ for _ in parse(s) if any_good(_)])


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (2)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (479)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (4)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (531)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
