#!/usr/bin/env python3

from colors import color
import itertools as it
import sympy
from fractions import Fraction

ExtraAsserts = False

ExampleInput1 = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

def parse(s):
    objects = []
    for line in s.splitlines():
        obj = []
        for xyz in line.split(' @ '):
            x, y, z = xyz.split(', ')
            if ExtraAsserts:
                obj.append((Fraction(x), Fraction(y), Fraction(z)))
            else:
                obj.append((float(x), float(y), float(z)))
        objects.append(tuple(obj))
    return objects

def part1_sympy_funcs():
    funcs = {}

    x, y, t = sympy.symbols('x, y, t')

    p_x, p_y, v_x, v_y = sympy.symbols('p_x, p_y, v_x, v_y')
    pv_2d = ((p_x, p_y), (v_x, v_y))
    eq1 = p_x + v_x * t - x
    teq_x = sympy.solve(eq1, t)
    assert len(teq_x) == 1
    teq_x = teq_x[0]
    funcs['t(x, pv_2d)'] = sympy.lambdify([x, pv_2d], teq_x)

    eq2 = eq1.subs(((x, y), (p_x, p_y), (v_x, v_y)))
    teq_y = sympy.solve(eq2, t)
    assert len(teq_y) == 1
    teq_y = teq_y[0]
    yeq = sympy.solve(teq_x - teq_y, y)
    assert len(yeq) == 1
    yeq = yeq[0]
    funcs['y(x, pv_2d)'] = sympy.lambdify([x, pv_2d], yeq)

    p_1x, p_1y, v_1x, v_1y = sympy.symbols('p_1x, p_1y, v_1x, v_1y')
    pv_2d_1 = ((p_1x, p_1y), (v_1x, v_1y))
    vars_1 = tuple(zip((s for p in pv_2d for s in p), (s for p in pv_2d_1 for s in p)))
    yeq_1 = yeq.subs(vars_1)

    p_2x, v_2x, p_2y, v_2y = sympy.symbols('p_2x, v_2x, p_2y, v_2y')
    pv_2d_2 = ((p_2x, p_2y), (v_2x, v_2y))
    vars_2 = tuple(zip((s for p in pv_2d for s in p ), (s for p in pv_2d_2 for s in p)))
    yeq_2 = yeq.subs(vars_2)

    xeq = sympy.solve(yeq_1 - yeq_2, x)
    assert len(xeq) == 1
    xeq = xeq[0]
    funcs['x(a2d, b2d)'] = sympy.lambdify([pv_2d_1, pv_2d_2], xeq)

    return funcs

def count_pairwise_xy_path_intersections(objects, test_range):
    count = 0
    past_count = 0
    parallel_count = 0
    outside_count = 0

    funcs = part1_sympy_funcs()

    for pairno, (a, b) in enumerate(it.combinations(objects, 2)):

        a2d = tuple(_[0:2] for _ in a)
        b2d = tuple(_[0:2] for _ in b)

        # print()
        # print(f"Hailstone A: {a[0]} @ {a[1]}")
        # print(f"Hailstone B: {b[0]} @ {b[1]}")

        try:
            x = funcs['x(a2d, b2d)'](a2d, b2d)
            y = funcs['y(x, pv_2d)'](x, a2d)
            ta = funcs['t(x, pv_2d)'](x, a2d)
            tb = funcs['t(x, pv_2d)'](x, b2d)
        except ZeroDivisionError:
            parallel_count += 1
            continue

        if ta < 0 or tb < 0:
            past_count += 1
            # which = "Hailstone A"
            # if tb < 0:
            #     if ta < 0:
            #         which = "both hailstones"
            #     else:
            #         which = "Hailstone B"
            # print(f"Hailstones' paths crossed in the past for {which}.")
            continue

        if test_range.start <= x < test_range.stop and test_range.start <= y < test_range.stop:
            # print("Hailstones' paths will cross", color("inside", "#ffffff"), f"the test area (at {x=}, {y=}).")
            count += 1
            continue

        # print(f"Hailstones' paths will cross outside the test area (at {x=},{y=}).")
        outside_count += 1

    return count


def part1(s):
    objects = parse(s)
    return count_pairwise_xy_path_intersections(objects, range(200000000000000, 400000000000001))
    return "TODO"


def part2(s):
    return "TODO"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(count_pairwise_xy_path_intersections(parse(ExampleInput1), range(7, 28)))

    print()
    print("Part 1")
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
