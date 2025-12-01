#!/usr/bin/env python3

MultiLineExample = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

ExamplesPart1 = (
    (MultiLineExample, 3),
)

ExamplesPart2 = (
    (MultiLineExample, 6),
    ("R1000", 10),
    ("L50", 1),
    ("L51", 1),
    ("L100", 1),
    ("L101", 1),
    ("L150", 2),
    ("L151", 2),
    ("R49", 0),
    ("R50", 1),
    ("R51", 1),
    ("R100", 1),
    ("L50\nR100", 2),
)


def part1(s):
    c = 0
    n = 50
    for line in s.splitlines():
        d, x = line[0], int(line[1:])
        if d == 'L':
            x = -x
        n = (n + x) % 100
        if n == 0:
            c += 1
    return c


def part2(s):
    c = 0
    n = 50
    for line in s.splitlines():
        d, x = line[0], int(line[1:])

        zeros = 0
        if d == 'L':
            base = 1
            if n == 0:
                base = 0
            if x >= n:
                zeros = base + (x - n) // 100
            n = (n - x) % 100
        else:
            if (x + n) >= 100:
                zeros = (x + n) // 100
            n = (n + x) % 100
        c += zeros
    return c


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

    print("Part 1 (1086)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (6268)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
