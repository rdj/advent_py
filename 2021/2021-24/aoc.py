#!/usr/bin/env python3

# Generally, see input-annotated.txt.
# A lot of this is from grokking the assembly-like input.
# It runs the same subroutine for each of the input digits.
# Each digit takes in the result of the previous digit.
# The subroutine differs for each digit in the form of three literal ints.
# The parse function slurps out the three literal ints that differ for each digit.
def parse(s):
    subs = s.split("\ninp")

    params = []
    for sub in subs:
        lines = sub.splitlines()
        params.append(tuple(int(line.split()[-1]) for line in (lines[4], lines[5], lines[15])))
    return tuple(params)


# Literal implementation of the subroutine
def zsub0(w, z, params):
    # inp w

    # mul x 0
    x = 0
    # add x z
    x += z
    # mod x 26
    x %= 26
    # div z ?
    z //= params[0]
    # add x ?
    x += params[1]
    # eql x w
    x = int(x == w)
    # eql x 0
    x = int(x == 0)

    # mul y 0
    y = 0
    # add y 25
    y += 25
    # mul y x
    y *= x
    # add y 1
    y += 1
    # mul z y
    z *= y

    # mul y 0
    y = 0
    # add y w
    y += w
    # add y ?
    y += params[2]
    # mul y x
    y *= x

    # add z y
    z += y

    return z


# Refactored version of subroutine, verified with
#     for p in params:
#         for z in range(0, 26):
#             for w in range(1, 10):
#                 assert(zsub(w, z, p) == zsub0(w, z, p))
def zsub(w, z, params):
    x = z % 26 + params[1]
    z //= params[0]
    if not x == w:
        z = 26*z + w + params[2]
    return z


# There are 14 subroutines.
# 7 of them always divide z by 26.
# All of them conditionally multiply z by 26.
# We are probably hosed if we multiply by 26 more times than we divide by it.
# We can only prevent the multiplication when param[1] < 10.
# Not coincidentally, 7 subroutines have param[1] < 10.
# So we must ensure that the condition is met for those 7 digits.
# Note that this does not enforce 0 < w < 10.
def solvew(z, params):
    if params[1] >= 10:
        return None
    return z % 26 + params[1]


def findcode(z, params, digits, biggest=True):
    if not params:
        if z == 0:
            return "".join(map(str, digits))
        else:
            return None

    wrange = None
    p = params[0]

    w = solvew(z, p)
    if w is not None:
        if w < 1 or w > 9:
            return None
        wrange = (w,)

    if wrange is None:
        wrange = range(1, 10)
        if biggest:
            wrange = reversed(wrange)

    for w in wrange:
        code = findcode(zsub(w, z, p), params[1:], digits + (w,), biggest)
        if code:
            return code
    return None


def part1(s):
    return findcode(0, parse(s), tuple())


def part2(s):
    return findcode(0, parse(s), tuple(), biggest=False)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (79197919993985)")
    print(part1(real_input()))

    print()
    print("Part 2 (13191913571211)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
