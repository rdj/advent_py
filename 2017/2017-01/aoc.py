#!/usr/bin/env pypy3


ExamplesPart1 = (
    ("1122", 3),
    ("1111", 4),
    ("1234", 0),
    ("91212129", 9),
)

ExamplesPart2 = (
    ("1212", 6),
    ("1221", 0),
    ("123425", 4),
    ("123123", 12),
    ("12131415", 4),
)


def parse(s):
    return list(map(int, s.strip()))


def compute(d, rot):
    return sum(d[i] for i in range(len(d)) if d[i] == d[(i+rot) % len(d)])


def part1(s):
    return compute(parse(s), 1)


def part2(s):
    d = parse(s)
    return compute(d, len(d)//2)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        print(f"Example {i+1} Part 1 ({b})")
        print(part1(a))
        print()

    print("Part 1 (1136)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        print(f"Example {i+1} Part 2 ({b})")
        print(part2(a))
        print()

    print("Part 2 (1092)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
