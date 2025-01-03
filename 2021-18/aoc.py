#!/usr/bin/env pypy3

from functools import reduce
from itertools import permutations
from copy import deepcopy


ExampleInput1 = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


def mag(norp):
    if isinstance(norp, int):
        return norp
    a, b = norp
    return 3*mag(a) + 2*mag(b)


def split(p):
    for i in range(len(p)):
        if isinstance(p[i], int):
            n = p[i]
            if n > 9:
                p[i] = [n//2, (n+1)//2]
                return True
        elif split(p[i]):
            return True


def carryright(p, out):
    for i in range(len(p)):
        if out['carryright'] == 0:
            return

        if isinstance(p[i], int):
            p[i] += out['carryright']
            out['carryright'] = 0
            return
        carryright(p[i], out)


def carryleft(p, out):
    for i in range(len(p)-1, -1, -1):
        if out['carryleft'] == 0:
            return

        if isinstance(p[i], int):
            p[i] += out['carryleft']
            out['carryleft'] = 0
            return
        carryleft(p[i], out)


def explode(p, d=0):
    for i in range(len(p)):
        if not isinstance(p[i], int):
            out = None

            if d == 3:
                e = p[i]
                assert(isinstance(e[0], int))
                assert(isinstance(e[1], int))
                out = {'carryleft': e[0], 'carryright': e[1]}
                p[i] = 0
            else:
                out = explode(p[i], d+1)

            if out:
                if i == 0:
                    if isinstance(p[1], int):
                        p[1] += out['carryright']
                        out['carryright'] = 0
                    else:
                        carryright(p[1], out)
                else:
                    if isinstance(p[0], int):
                        p[0] += out['carryleft']
                        out['carryleft'] = 0
                    else:
                        carryleft(p[0], out)
                return out


def red(p):
    while True:
        while explode(p):
            pass
        if not split(p):
            return False


def parse(s):
    return list(map(eval, s.splitlines()))


def snailadd(a, b):
    c = [deepcopy(a), deepcopy(b)]
    red(c)
    return c


def part1(s):
    return mag(reduce(snailadd, parse(s)))


def part2(s):
    return max(map(lambda s: mag(snailadd(*s)), permutations(parse(s), 2)))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (4140)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (4202)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (3993)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (4779)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
