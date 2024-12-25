#!/usr/bin/env pypy3

ExampleInput1 = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def parse(s):
    locks = []
    keys = []

    blocks = [b.splitlines() for b in s.split("\n\n")]
    w = len(blocks[0][0])
    h = len(blocks[0])

    for b in blocks:
        dst = locks
        if all(c == '#' for c in b[-1]):
            dst = keys
            b = list(reversed(b))

        heights = []
        for j in range(w):
            for i in range(h):
                if b[i][j] == '.':
                    break
            heights.append(i - 1)
        dst.append(tuple(heights))

    return locks, keys, h - 2


def part1(s):
    locks, keys, height = parse(s)

    fits = 0
    for lock in locks:
        for key in keys:
            if all(n <= height for n in map(sum, zip(lock, key))):
                fits += 1

    return fits


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (3)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (2900)")
    print(part1(real_input()))


if __name__ == "__main__":
    run_all()
