#!/usr/bin/env pypy3

from collections import deque


ExampleInput1 = """\
5
"""


def part1(s):
    size = int(s.strip())
    d = deque(range(1, size+1))

    while len(d) > 1:
        a = d.popleft()
        b = d.popleft()
        d.append(a)

    return d[0]


def part2(s):
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
    print(part2("5"))#ExampleInput1))

    print()
    print("Part 2 (1407007)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()

