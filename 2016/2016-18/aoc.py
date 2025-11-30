#!/usr/bin/env python3

ExamplesPart1 = (
    ("..^^.\n", 3, 6),
    (".^^.^.^^^^\n", 10, 38),
)


def part1(s, rows=40):
    s = s.strip()

    bitlen = len(s)
    mask = (1 << bitlen) - 1

    n = int(s.translate(str.maketrans(".^", "01")), 2)
    bad = n.bit_count()
    #print(format(n, f"0{bitlen}b"))
    for _ in range(rows-1):
        n = (n << 1 ^ n >> 1) & mask
        #print(format(n, f"0{bitlen}b"))
        bad += n.bit_count()

    return bitlen * rows - bad


def part2(s):
    return part1(s, 400_000)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, rows, b) in enumerate(ExamplesPart1):
        c = part1(a, rows)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (2035)")
    print(part1(real_input()))
    print()

    print("Part 2")
    print(part2(real_input()))
    print()


if __name__ == "__main__":
    run_all()
