#!/usr/bin/env python3

from collections import defaultdict

ExampleInput1 = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip()


def parse_line(s):
    game = {}
    game_str, rounds_str = s.split(': ')
    game['id'] = int(game_str.split()[-1])
    game['rounds'] = []
    for rs in rounds_str.split('; '):
        r = {}
        for cs in rs.split(', '):
            num, col = cs.split();
            r[col] = int(num)
        game['rounds'].append(r)
    return game


def parse(s):
    return [parse_line(_) for _ in s.splitlines()]


def maxcolors(game):
    m = defaultdict(int)
    for r in game['rounds']:
        for col, num in r.items():
            m[col] = max(m[col], num)
    return m


def part1_valid(g):
    maxes = maxcolors(g)
    for col, num in { 'red': 12, 'green': 13, 'blue': 14 }.items():
        if maxes[col] > num:
            return False
    return True


def part1(s):
    return sum([g['id'] for g in parse(s) if part1_valid(g)])


def power(m):
    return m['red'] * m['green'] * m['blue']


def part2(s):
    return sum(power(maxcolors(g)) for g in parse(s))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read().strip()


def run_all():
    print("Example Part 1 (8)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (2156)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2286)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (66909)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
