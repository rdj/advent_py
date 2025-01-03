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


ExampleInput2 = """\
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
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


def explode(p, d=0, leftone=None):
    if leftone == None:
        leftone = {}

    for i in range(len(p)):
        if isinstance(p[i], int):
            leftone['p'] = p
            leftone['i'] = i
        else:
            out = None

            if d == 3:
                e = p[i]
                assert(isinstance(e[0], int))
                assert(isinstance(e[1], int))
                out = {'carryright': e[1]}
                if leftone:
                    leftone['p'][leftone['i']] += e[0]
                p[i] = 0
            else:
                out = explode(p[i], d+1, leftone)

            if out:
                if i == 0:
                    if isinstance(p[1], int):
                        p[1] += out['carryright']
                        out['carryright'] = 0
                    else:
                        carryright(p[1], out)
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
    print("Example 2 Part 1 (3488)")
    print(part1(ExampleInput2))

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
