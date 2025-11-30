#!/usr/bin/env python3

from collections import deque


ExamplesPart1 = (
    ("{}", 1),
    ("{{{}}}", 6),
    ("{{},{}}", 5),
    ("{{{},{},{{}}}}", 16),
    ("{<a>,<a>,<a>,<a>}", 1),
    ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
    ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
    ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3),
)


def skip_garbage(toks):
    chars = 0
    while True:
        match toks.popleft():
            case "!":
                toks.popleft()

            case ">":
                return chars

            case _:
                chars += 1


def score(toks, depth=1):
    points = depth
    garbage = 0
    while True:
        match toks.popleft():
            case "{":
                p, g = score(toks, depth + 1)
                points += p
                garbage += g
            case "<":
                garbage += skip_garbage(toks)
            case "}":
                return points, garbage
            case comma:
                # This parser is lax about extra commas but I think that should be fine
                assert(comma == ",")


def part1(s):
    toks = deque(s.strip())
    assert("{" == toks.popleft())
    return score(toks)[0]


def part2(s):
    toks = deque(s.strip())
    assert("{" == toks.popleft())
    return score(toks)[1]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (s, x) in enumerate(ExamplesPart1):
        print(f"Example Part 1.{i} ({x})")
        print(part1(s))
        print()

    print("Part 1 (8337)")
    print(part1(real_input()))
    print()

    print("Part 2 (4330)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()

