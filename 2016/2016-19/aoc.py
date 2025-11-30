#!/usr/bin/env python3

from collections import deque
from math import log


ExampleInput1 = """\
5
"""


def part1sim(s):
    size = int(s.strip())
    d = deque(range(1, size+1))

    while len(d) > 1:
        a = d.popleft()
        b = d.popleft()
        d.append(a)

    return d[0]


# The OEIS entry for part 2 referenced Josephus Problem:
#
#     https://en.wikipedia.org/wiki/Josephus_problem
#     https://oeis.org/A006257
#
# The title of today's Avent of Code puzzle is An Elephant Named Joseph, so
# that's definitely on purpose. This thing dates back to the first century CE.
#
# Anyway, might as well to a math version.
#
def part1math(s):
    size = int(s.strip())
    log2 = int(log(size, 2))
    base = 2 ** log2
    n = size - base
    return 2*n + 1


def part1(s):
    return part1math(s)


# I'm leaving the simulated version since it really did take some thought to
# come up with this implementation that focuses on the center of the list.
def part2sim(s):
    size = int(s.strip())

    front = deque(range(1, size//2 + 1))
    back = deque(range(size//2 + 1, size + 1))

    while front and back:
        if len(front) > len(back):
            b = front.pop()
        else:
            b = back.popleft()

        a = front.popleft()
        # print("{a} steals from {b}")
        back.append(a)
        front.append(back.popleft())

    return (front or back)[0]


# I can't really explain this; I just printed out solutions and came up with a
# closed form solution. The solutions reset back to 1 after powers of three,
# then count up by one halfway to the next power of three, then count up by two
# for the second half:
#
#    1:     1
#
#    2:     1
#    3:     3
#
#    4:     1 (reset after 3**1, count by +1)
#    5:     2
#    6:     3
#    7:     5 (second half, count by +2)
#    8:     7
#    9:     9
#
#    ... Up to 27 ...
#    1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27
#    ... after that it resets and builds back to 81, etc. ...
#
# Later, I checked OEIS and sure enough this sequence is documented as
# "The n-cowboy shootout problem".
#
#     https://oeis.org/A334473
#
def part2math(s):
    size = int(s.strip())
    log3 = int(log(size, 3))
    base = 3 ** log3
    n = size - base
    if n == 0:
        return base
    if n < base:
        return n
    return base + (n - base) * 2


def part2(s):
    return part2math(s)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (3)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (1808357)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1407007)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()

