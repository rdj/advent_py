#!/usr/bin/env python3

from colors import color
import functools as ft
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

@ft.cache
def part1_sympy_equations():
    results = {}

    x, y, t = sympy.symbols('x, y, t')

    p_x, v_x, p_y, v_y = sympy.symbols('p_x, v_x, p_y, v_y')
    eq1 = p_x + v_x * t - x
    teq_x = sympy.solve(eq1, t)
    assert len(teq_x) == 1
    teq_x = teq_x[0]

    eq2 = eq1.subs(((x, y), (p_x, p_y), (v_x, v_y)))
    teq_y = sympy.solve(eq2, t)
    assert len(teq_y) == 1
    teq_y = teq_y[0]
    yeq = sympy.solve(teq_x - teq_y, y)
    assert len(yeq) == 1
    yeq = yeq[0]

    p_1x, v_1x, p_1y, v_1y = sympy.symbols('p_1x, v_1x, p_1y, v_1y')
    vars_1 = tuple(zip((p_x, v_x, p_y, v_y), (p_1x, v_1x, p_1y, v_1y)))
    yeq_1 = yeq.subs(vars_1)
    results['yeq_1'] = yeq_1

    p_2x, v_2x, p_2y, v_2y = sympy.symbols('p_2x, v_2x, p_2y, v_2y')
    vars_2 = tuple(zip((p_x, v_x, p_y, v_y), (p_2x, v_2x, p_2y, v_2y)))
    yeq_2 = yeq.subs(vars_2)
    results['yeq_2'] = yeq_2

    xeq = sympy.solve(yeq_1 - yeq_2, x)
    assert len(xeq) == 1
    xeq = xeq[0]
    results['xeq'] = xeq

    results['teq_1x'] = teq_x.subs(vars_1)
    results['teq_1y'] = teq_y.subs(vars_1)
    results['teq_2x'] = teq_x.subs(vars_2)
    results['teq_2y'] = teq_y.subs(vars_2)

    results['params'] = (p_1x, p_1y, v_1x, v_1y, p_2x, p_2y, v_2x, v_2y)
    results['sym'] = { 'x': x, 'y': y, 't': y }

    print(results)

    return results

def part1_sympy_result(a, b):
    eqs = part1_sympy_equations()
    results = {}

    x = eqs['sym']['x']
    y = eqs['sym']['y']

    values = tuple(zip(eqs['params'], (a[0][0], a[0][1], a[1][0], a[1][1], b[0][0], b[0][1], b[1][0], b[1][1])))
    xval = eqs['xeq'].subs(values)
    if xval.is_infinite:
        # Denominator is 0, parallel lines
        return {}
    results['x'] = xval

    yval_1 = eqs['yeq_1'].subs(values).subs(x, xval)
    results['y'] = yval_1
    yval = yval_1

    if ExtraAsserts:
        yval_2 = eqs['yeq_2'].subs(values).subs(x, xval)
        if abs(yval_1 - yval_2) > 1:
            print(color(f"{a=}, {b=}: Y value mismatch {yval_1=} {yval_2=} {abs(yval_1 - yval_2)=}", 'red'))

    tval_1x = eqs['teq_1x'].subs(values).subs(x, xval)
    if ExtraAsserts:
        tval_1y = eqs['teq_1y'].subs(values).subs(y, yval)
        assert abs(tval_1x - tval_1y) < 1
    results['ta'] = tval_1x

    tval_2x = eqs['teq_2x'].subs(values).subs(x, xval)
    if ExtraAsserts:
        tval_2y = eqs['teq_2y'].subs(values).subs(y, yval)
        assert abs(tval_2x - tval_2y) < 1
    results['tb'] = tval_2x

    return results

def count_pairwise_xy_path_intersections(objects, test_range):
    count = 0
    past_count = 0
    parallel_count = 0
    outside_count = 0

    for pairno, (a, b) in enumerate(it.combinations(objects, 2)):

        # So I kept just typo'ing variables or something, so I ended up solving
        # this in sympy so I could copy/paste the relevant equations in, then
        # everything was fine. These are the same ones I came up with by hand,
        # then again the same ones I verified with Wolfram Alpha, but I kept
        # messing something up. Sympy to the rescue. Of course, sympy is too
        # slow to do the real input, but all we need is the closed form
        # solution:
        #
        # y_1 = (-p_1x*v_1y + p_1y*v_1x + v_1y*x)/v_1x
        # y_2 = (-p_2x*v_2y + p_2y*v_2x + v_2y*x)/v_2x,
        # x = (-p_1x*v_1y*v_2x + p_1y*v_1x*v_2x + p_2x*v_1x*v_2y - p_2y*v_1x*v_2x)/(v_1x*v_2y - v_1y*v_2x)
        # t_1x = (-p_1x + x)/v_1x
        # t_1y = (-p_1y + y)/v_1y
        # t_2x = (-p_2x + x)/v_2x
        # t_2y = (-p_2y + y)/v_2y

        (p_1x, p_1y, p_1z), (v_1x, v_1y, v_1z) = a
        (p_2x, p_2y, p_2z), (v_2x, v_2y, v_2z) = b

        # print()
        # print(f"Hailstone A: {a[0]} @ {a[1]}")
        # print(f"Hailstone B: {b[0]} @ {b[1]}")

        xden = v_1x*v_2y - v_1y*v_2x
        if xden == 0:
            parallel_count += 1
            # print("Hailstones' paths are parallel; they never intersect.")
            continue

        x = (-p_1x*v_1y*v_2x + p_1y*v_1x*v_2x + p_2x*v_1x*v_2y - p_2y*v_1x*v_2x) / xden
        y = (-p_1x*v_1y + p_1y*v_1x + v_1y*x)/v_1x
        ta = (-p_1x + x)/v_1x
        tb = (-p_2x + x)/v_2x

        if ExtraAsserts:
            assert y == (-p_2x*v_2y + p_2y*v_2x + v_2y*x)/v_2x
            assert ta == (-p_1y + y)/v_1y
            assert tb == (-p_2y + y)/v_2y

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
