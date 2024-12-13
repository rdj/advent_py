#!/usr/bin/env pypy3

from more_itertools import chunked
import re
import z3


ExampleInput1 = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

def parse(s):
    games = []
    for lines in chunked(s.splitlines(), 4):
        game = []
        for line in lines[:3]:
            x, y = re.search(r'X[+=](\d+), Y[+=](\d+)', line).groups()
            game.append((int(x), int(y)))
        games.append(game)
    return games


def part1(s):
    tokens = 0
    games = parse(s)

    for g in games:
        a = z3.Int('a')
        b = z3.Int('b')
        opt = z3.Optimize()
        opt.add(a <= 100, b <= 100, a >= 0, b >= 0)
        opt.add(a * g[0][0] + b * g[1][0] == g[2][0])
        opt.add(a * g[0][1] + b * g[1][1] == g[2][1])
        opt.minimize(3*a + b)
        if opt.check() == z3.sat:
            m = opt.model()
            tokens += 3*m[a] + m[b]

    return z3.simplify(tokens)


def part2(s):
    tokens = 0
    games = parse(s)

    BIG = 10000000000000

    for g in games:
        a = z3.Int('a')
        b = z3.Int('b')
        opt = z3.Optimize()
        opt.add(a >= 0, b >= 0)
        opt.add(a * g[0][0] + b * g[1][0] == (BIG + g[2][0]))
        opt.add(a * g[0][1] + b * g[1][1] == (BIG + g[2][1]))
        opt.minimize(3*a + b)
        if opt.check() == z3.sat:
            m = opt.model()
            tokens += 3*m[a] + m[b]

    return z3.simplify(tokens)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (480)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (27157)")
    print(part1(real_input()))

    print()
    print("Part 2 (104015411578548)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
