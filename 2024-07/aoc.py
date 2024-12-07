#!/usr/bin/env pypy3

import operator as OP


ExampleInput1 = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def parse(s):
    eqs = []
    for line in s.splitlines():
        k, vs = line.split(": ")
        k = int(k)
        vs = [int(_) for _ in vs.split()]
        eqs.append((k, vs))
    return eqs


def is_good(target, nums, ops):
    if len(nums) == 1:
        return target == nums[0]

    a, b, *rest = nums
    if a > target:
        return False

    return any(is_good(target, [op(a, b)] + rest, ops) for op in ops)


def part1(s):
    return sum(k for k, v in parse(s) if is_good(k, v, [OP.add, OP.mul]))


def part2(s):
    return sum(k for k, v in parse(s) if is_good(k, v, [OP.add, OP.mul, lambda a, b: int(str(a)+str(b))]))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (3749)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (1298103531759)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (11387)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (140575048428831)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
