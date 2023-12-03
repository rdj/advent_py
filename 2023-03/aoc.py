#!/usr/bin/env python3

from collections import defaultdict

ExampleInput1 = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()


def is_adjacent(m, r, c):
    for r, c in [
        [r - 1, c - 1],
        [r - 1, c],
        [r - 1, c + 1],
        [r, c - 1],
        [r, c + 1],
        [r + 1, c - 1],
        [r + 1, c],
        [r + 1, c + 1]]:
        if r >= 0 and c >= 0 and r < len(m) and c < len(m[r]) and not m[r][c].isdigit() and m[r][c] != '.':
            return True
    return False


def gear_adjacent(m, r, c):
    for r, c in [
        [r - 1, c - 1],
        [r - 1, c],
        [r - 1, c + 1],
        [r, c - 1],
        [r, c + 1],
        [r + 1, c - 1],
        [r + 1, c],
        [r + 1, c + 1]]:
        if r >= 0 and c >= 0 and r < len(m) and c < len(m[r]) and m[r][c] == '*':
            return (r, c)
    return None


def part1(s):
    result = 0
    m = s.splitlines()
    a = ''
    adj = False
    for r in range(len(m)):
        for c in range(len(m[r])):
            if m[r][c].isdigit():
                a += m[r][c]
                adj = adj or is_adjacent(m, r, c)
            else:
                if a != '':
                    if adj:
                        result += int(a)
                    a = ''
                    adj = False
        if a != '':
            if adj:
                result += int(a)
            a = ''
            adj = False

    return result


def part2(s):
    gears = defaultdict(list)

    m = s.splitlines()
    a = ''
    gear = None
    for r in range(len(m)):
        for c in range(len(m[r])):
            if m[r][c].isdigit():
                a += m[r][c]
                g = gear_adjacent(m, r, c)
                if g != None:
                    if gear != None and g != gear:
                        raise Exception(f"More than one gear: ({r}, {c}), {g} {gear}")
                    gear = g
            else:
                if a != '':
                    if gear:
                        gears[gear].append(int(a))
                    a = ''
                    gear = None
        if a != '':
            if gear:
                gears[gear].append(int(a))
            a = ''
            gear = None

    result = 0
    for v in gears.values():
        if len(v) > 2:
            raise Exception("Too many gear things")
        if len(v) == 2:
            result += v[0] * v[1]

    return result

def real_input():
    with open("input.txt", "r") as infile:
        return infile.read().strip()


def run_all():
    print("Example Part 1 (4361)")
    print(part1(ExampleInput1))

    print()
    print("Part 1")
    print(part1(real_input()))

    print()
    print("Example Part 2 (467835)")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
