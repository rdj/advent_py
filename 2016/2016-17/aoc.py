#!/usr/bin/env pypy3


import _md5
from collections import deque


ExamplesPart1 = (
    ("ihgpwlah", "DDRRRD"),
    ("kglvqrro", "DDUDRLRRUDRD"),
    ("ulqzkmiv", "DRURDRUDDLLDLUURRDULRLDUUDDDRR"),
)


ExamplesPart2 = (
    ("ihgpwlah", 370),
    ("kglvqrro", 492),
    ("ulqzkmiv", 830),
)


def md5(s):
    return _md5.md5(s, usedforsecurity=False).hexdigest()


DIRS = (
    (b"U", (0, -1)),
    (b"D", (0, 1)),
    (b"L", (-1, 0)),
    (b"R", (1, 0)),
)


def find_path(s, longest=False):
    xf, yf = 3, 3
    seed = bytes(s.strip(), "ascii")
    solution = None

    q = deque([(b"", (0, 0))])
    while q:
        path, (x, y) = q.popleft()
        h = md5(seed + path)

        for i, (d, (dx, dy)) in enumerate(DIRS):
            if h[i] not in "bcdef":
                continue
            x1, y1 = x + dx, y + dy
            if not (0 <= x1 <= xf and 0 <= y <= yf):
                continue
            newpath = path + d
            if (x1, y1) == (xf, yf):
                solution = str(newpath, "ascii")
                if not longest:
                    return solution
            else:
                q.append((newpath, (x1, y1)))

    return solution


def part1(s):
    return find_path(s)


def part2(s):
    return len(find_path(s, longest=True))


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

    print("Part 1 (DURLDRRDRD)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()


    print("Part 2 (650)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
