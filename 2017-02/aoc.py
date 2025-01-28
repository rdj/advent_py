#!/usr/bin/env pypy3


ExampleInput1 = """\
5 1 9 5
7 5 3
2 4 6 8
"""

ExampleInput2 = """\
5 9 2 8
9 4 7 3
3 8 6 5
"""

def parse(s):
    return [list(map(int, line.split())) for line in s.splitlines()]


def part1(s):
    return sum(abs(max(a) - min(a)) for a in parse(s))


def row(a):
    a = sorted(a)
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            q, r = divmod(a[j], a[i])
            if r == 0:
                return q


def part2(s):
    return sum(map(row, parse(s)))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (18)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (47623)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (9)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (312)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
