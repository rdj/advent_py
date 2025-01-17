#!/usr/bin/env pypy3


ExamplesPart1 = [
    ("0,3,6", 436),
    ("1,3,2", 1),
    ("2,1,3", 10),
    ("1,2,3", 27),
    ("2,3,1", 78),
    ("3,2,1", 438),
    ("3,1,2", 1836),
]

ExamplesPart2 = [
    ("0,3,6", 175594),
    ("1,3,2", 2578),
    ("2,1,3", 3544142),
    ("1,2,3", 261214),
    ("2,3,1", 6895259),
    ("3,2,1", 18),
    ("3,1,2", 362),
]


# Runtime with dict is 8s for part2. Switching to a pre-allocated array reduces
# it to to 475ms. Turns out the number of iterations is a good size for the
# array. Can start with smaller at the cost of some resizing. For example,
# starting with the array of size max(iv) + 1 takes about twice as long.
def part1(s, nth=2020):
    iv = list(map(int, s.split(",")))
    seen = [-1] * nth
    prev = None

    for i in range(len(iv)):
        n = iv[i]
        if prev != None:
            seen[prev] = i
        prev = n

    for i in range(len(iv), nth):
        if prev >= len(seen):
            seen += [-1] * (prev - len(seen) + 1)
        s = seen[prev]
        if s == -1:
            n = 0
        else:
            n = i - s

        seen[prev] = i
        prev = n

    return n


def part2(s):
    return part1(s, nth=30_000_000)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (s, e) in enumerate(ExamplesPart1):
        print(f"Example {i+1} Part 1 ({e})")
        print(part1(s))
        print()

    print("Part 1 (260)")
    print(part1(real_input()))
    print()

    for i, (s, e) in enumerate(ExamplesPart2):
        print(f"Example {i+1} Part 2 ({e})")
        print(part2(s))
        print()

    print("Part 2 (950)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
