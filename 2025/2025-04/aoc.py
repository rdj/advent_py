#!/usr/bin/env python3

MultiLineExample = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

ExamplesPart1 = (
    (MultiLineExample, 13),
)

ExamplesPart2 = (
    (MultiLineExample, 43),
)


def parse(s):
    grid = []
    lines = s.splitlines()
    padrow = [0] * (len(lines[0]) + 2)

    grid.append(padrow)
    for line in s.splitlines():
        grid.append([c == '@' for c in '.'+line+'.'])
    grid.append(padrow)

    return grid


def neighbors(x, y):
    for dx, dy in ((-1, -1), (-1, 0), (-1, 1),
                   ( 0, -1),          ( 0, 1),
                   ( 1, -1), ( 1, 0), ( 1, 1)):
        x1, y1 = x + dx, y + dy
        yield x1, y1


def accessible(grid, x0, y0):
    if grid[y0][x0]:
        return sum(grid[y1][x1] for x1, y1 in neighbors(x0, y0)) < 4
    return 0


def part1(s):
    grid = parse(s)
    return sum(accessible(grid, x, y) for x in range(len(grid)) for y in range(len(grid)))


def runonce(grid):
    togo = list((x, y) for x in range(len(grid)) for y in range(len(grid)) if accessible(grid, x, y))
    for x, y in togo:
        grid[y][x] = 0
    return len(togo)


def part2(s):
    g = parse(s)
    t = 0
    while r := runonce(g):
        t += r
    return t


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

    print("Part 1 (1372)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 ()")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
