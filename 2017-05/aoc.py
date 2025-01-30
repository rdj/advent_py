#!/usr/bin/env pypy3

## Things I used in previous years

# from colors import color  ## pip install py-colors
# from collections import Counter
# from collections import defaultdict
# from collections import deque
# from colors import color
# from enum import Enum
# from fractions import Fraction
# from functools import cached_property
# from functools import lru_cache
# from functools import reduce
# from functools import reduce, partial
# from heapq import heappush, heappop
# from itertools import pairwise
# from math import prod
# from more_itertools import chunked, sliding_window
# from multiprocessing import Pool
# from numpy import transpose
# from operator import mul
# from pathlib import Path
# from typing import NamedTuple
# import cProfile
# import functools as ft
# import itertools as it
# import math
# import networkx as nx
# import operator as op
# import pygraphviz as pgv
# import re
# import sympy


from itertools import count


ExampleInput1 = """\
0
3
0
1
-3
"""


def parse(s):
    return list(map(int, s.splitlines()))


def run(s, getoffset):
    a = parse(s)
    ip = 0

    try:
        for steps in count():
            j = a[ip]
            a[ip] += getoffset(j)
            ip += j
    except IndexError:
        return steps


def part1(s):
    return run(s, lambda j: 1)


def part2(s):
    return run(s, lambda j: -1 if j >= 3 else 1)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (5)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (364539)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (10)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (27477714)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
