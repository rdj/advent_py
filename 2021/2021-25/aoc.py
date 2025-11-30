#!/usr/bin/env python3


ExampleInput1 = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""


def parse(s):
    east = set()
    south = set()

    lines = s.splitlines()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case 'v':
                    south.add((x, y))
                case '>':
                    east.add((x, y))

    return east, south, len(lines[0]), len(lines)


def part1(s):
    east, south, w, h = parse(s)
    last = None
    steps = 0

    while True:
        movecount = 0

        for src, (dx, dy) in ((east, (1, 0)), (south, (0, 1))):
            moving = []
            for p in src:
                x, y = p
                n = ((x + dx) % w, (y + dy) % h)
                if n in east or n in south:
                    continue
                moving.append((p, n))
            movecount += len(moving)
            for p, n in moving:
                src.remove(p)
                src.add(n)

        steps += 1
        if movecount == 0:
            return steps


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (58)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (523)")
    print(part1(real_input()))


if __name__ == "__main__":
    run_all()
