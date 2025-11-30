#!/usr/bin/env python3

ExamplesPart1 = (
    ("R2, L3", 5),
    ("R2, R2, R2", 2),
    ("R5, L5, R5, R3", 12),
)

ExamplesPart2 = (
    ("R8, R4, R4, R8", 4),
)


def parse(s):
    return tuple((one[0], int(one[1:])) for one in s.split(", "))


def part1(s):
    dirs = parse(s)
    x, y = 0, 0
    dx, dy = 0, -1

    for t, n in dirs:
        match t:
            case "L":
                dx, dy = dy, -dx
            case "R":
                dx, dy = -dy, dx
        x += dx * n
        y += dy * n

    return abs(x) + abs(y)


def part2(s):
    dirs = parse(s)
    x, y = 0, 0
    dx, dy = 0, -1
    seen = set((x, y))

    for t, n in dirs:
        match t:
            case "L":
                dx, dy = dy, -dx
            case "R":
                dx, dy = -dy, dx
        for _ in range(n):
            x += dx
            y += dy
            if (x, y) in seen:
                return abs(x) + abs(y)
            seen.add((x, y))

    raise Exception("No repeated location found")


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        print(f"Example Part 1.{i} ({b})")
        print(part1(a))
        print()

    print("Part 1 (291)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        print(f"Example Part 2.{i} ({b})")
        print(part2(a))
        print()

    print("Part 2 (159)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
