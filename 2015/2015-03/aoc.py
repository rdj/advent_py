#!/usr/bin/env python3

ExamplesPart1 = (
    (">", 2),
    ("^>v<", 4),
    ("^v^v^v^v^v", 2),
)

ExamplesPart2 = (
    ("^v", 3),
    ("^>v<", 3),
    ("^v^v^v^v^v", 11),
)


def getdir(c):
    match c:
        case ">":
            return 1, 0
        case "<":
            return -1, 0
        case "^":
            return 0, -1
        case "v":
            return 0, 1


def visit(dirs, visited=None):
    if visited is None:
        visited = set()

    x, y = 0, 0
    visited.add((x,y))

    for d in dirs:
        dx, dy = getdir(d)
        x, y = x + dx, y + dy
        visited.add((x,y))

    return visited


def part1(s):
    return len(visit(s.strip()))


def part2(s):
    dirs = s.strip()
    visited = visit(dirs[::2])
    visit(dirs[1::2], visited)
    return len(visited)


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

    print("Part 1 (2081)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (2341)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
