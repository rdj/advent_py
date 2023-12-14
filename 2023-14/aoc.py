#!/usr/bin/env python3

from numpy import transpose
from collections import defaultdict

ExampleInput1 = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def parse(s):
    return [list(_) for _ in s.splitlines()]


def tilt_north(tiles):
    for y in range(len(tiles)):
        for x in range(len(tiles[0])):
            if tiles[y][x] == 'O':
                y0 = y
                while y0 - 1 >= 0 and tiles[y0 - 1][x] == '.':
                    tiles[y0][x] = '.'
                    y0 -= 1
                    tiles[y0][x] = 'O'


def calc_load(tiles):
    total = 0
    for y in range(len(tiles)):
        for x in range(len(tiles[0])):
            if tiles[y][x] == 'O':
                total += len(tiles) - y
    return total


def rotate_clockwise(src):
    dst = transpose(src).tolist()
    for r in dst:
        r.reverse()
    return dst


def do_cycle(tiles):
    tilt_north(tiles)
    tiles = rotate_clockwise(tiles)
    tilt_north(tiles) # WEST
    tiles = rotate_clockwise(tiles)
    tilt_north(tiles) # SOUTH
    tiles = rotate_clockwise(tiles)
    tilt_north(tiles) # EAST
    tiles = rotate_clockwise(tiles)

    return tiles


def keyify(tiles):
    return "\n".join("".join(_) for _ in tiles)


def part1(s):
    tiles = parse(s)
    tilt_north(tiles)
    return calc_load(tiles)


CYCLE_THRESHHOLD = 2


def part2(s):
    tiles = parse(s)
    assert(len(tiles) == len(tiles[0]))

    first_seen = {}
    seen_count = defaultdict(int)
    load_history = []

    n = 0
    while True:
        tiles = do_cycle(tiles)
        load = calc_load(tiles)
        key = keyify(tiles)

        load_history.append(load)
        if key not in first_seen:
            first_seen[key] = n

        if seen_count[key] == CYCLE_THRESHHOLD:
            cycle_base = first_seen[key]

            cycle_len = 0
            for k, v in seen_count.items():
                if v == CYCLE_THRESHHOLD:
                    cycle_len += 1

            target = (1000000000 - cycle_base) % cycle_len
            return load_history[target + cycle_base - 1]

        seen_count[key] += 1
        n += 1

    return None


def dump(tiles):
    print("\n".join("".join(_) for _ in tiles))

def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (136)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (110821)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (64)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (83516)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()

    # src = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]
    # dump(src)
    # print("====")
    # src = rotate_clockwise(src)
    # dump(src)
    # print("====")
    # src = rotate_clockwise(src)
    # dump(src)
    # print("====")
    # src = rotate_clockwise(src)
    # dump(src)
    # print("====")
    # src = rotate_clockwise(src)
    # dump(src)
    # print("====")
    # src = rotate_clockwise(src)
    # dump(src)

