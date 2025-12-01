#!/usr/bin/env python3

from math import prod


MultiLineExample = """\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""

ExamplesPart1 = (
    (MultiLineExample, 7),
)

ExamplesPart2 = (
    (MultiLineExample, 336),
)


def parse(s):
    return list(s.splitlines())


def count_trees(lines, dx, dy):
    width = len(lines[0])
    trees = 0
    x = 0
    for y in range(0, len(lines), dy):
        if lines[y][x] == '#':
            trees += 1
        x = (x + dx) % width
    return trees


def part1(s):
    return count_trees(parse(s), 3, 1)


def part2(s):
    slopes = (
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    )
    lines = parse(s)
    return prod(map(lambda s: count_trees(lines, s[0], s[1]), slopes))


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

    print("Part 1 (223)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (3517401300)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
