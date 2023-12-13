#!/usr/bin/env python3

from numpy import transpose

ExampleInput1 = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def parse(s):
    blocks = []
    for block in s.split("\n\n"):
        blocks.append([list(line) for line in block.splitlines()])
    return blocks


def check_horz(tiles, mistakes_wanted=0):
    h = len(tiles)
    w = len(tiles[0])
    for mirror in range(1, h):
        mistakes = 0
        for ra, rb in zip(range(mirror - 1, -1, -1), range(mirror, h)):
            for c in range(w):
                if tiles[ra][c] != tiles[rb][c]:
                    mistakes += 1
                    if mistakes > mistakes_wanted:
                        break
            if mistakes > mistakes_wanted:
              break
        if mistakes == mistakes_wanted:
            return mirror

    return None


def check_vert(tiles, mistakes_wanted=0):
    tiles = transpose(tiles).tolist()
    return check_horz(tiles, mistakes_wanted)


def part1(s):
    total = 0
    for n, tiles in enumerate(parse(s)):
        h = check_horz(tiles)
        if h:
            total += 100 * h
            continue
        v = check_vert(tiles)
        if v:
            total += v
            continue
        assert False
    return total


def part2(s):
    total = 0
    for n, tiles in enumerate(parse(s)):
        h = check_horz(tiles, 1)
        if h:
            total += 100 * h
            continue
        v = check_vert(tiles, 1)
        if v:
            total += v
            continue
        assert False
    return total


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (405)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (29213)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (400)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (37453)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
