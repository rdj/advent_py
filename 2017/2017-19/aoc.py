#!/usr/bin/env python3


ExampleInput1 = """\
     |         \n\
     |  +--+   \n\
     A  |  C   \n\
 F---|----E|--+\n\
     |  |  |  D\n\
     +B-+  +--+\n\
"""


# Add 1-space buffer to eliminate (literal) edge cases
def parse(s):
    inner = tuple(tuple(" " + line + " ") for line in s.splitlines())
    buf = (" ",) * len(inner[0])
    return (buf,) + inner + (buf,)


def run(s):
    a = parse(s)
    y, x = 1, a[1].index("|") # Starts at line 1 because of the buffer
    dy, dx = 1, 0
    seen = []
    steps = 0

    while a[y][x] != " ":
        steps += 1
        y += dy
        x += dx

        match a[y][x]:
            case "+":
                # The input has extra spaces between all the lines so the
                # corners are very easy: there will always be a space in one
                # direction and the continuation of the route in the other
                dy, dx = dx, dy
                if a[y+dy][x+dx] == " ":
                    dy, dx = -dy, -dx

            case v if v.isalpha():
                seen.append(v)

    return "".join(seen), steps


def part1(s):
    return run(s)[0]


def part2(s):
    return run(s)[1]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (ABCDEF)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (GSXDIPWTU)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (38)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (16100)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
