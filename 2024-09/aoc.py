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


ExampleInput1 = """\
2333133121414131402
"""

Free = 2 << 31

def part1(s):
    s = s.splitlines()[0]
    size = sum(int(_) for _ in s)
    disk = [Free] * size

    cur = 0
    file = 0
    space = False
    for n in s:
        n = int(n)
        if space:
            cur += n
            space = False
            continue
        for _ in range(n):
            disk[cur] = file
            cur += 1
        file +=1
        space = True

    lcur = 0
    rcur = len(disk) - 1
    while True:
        while disk[lcur] != Free:
            lcur += 1
        while disk[rcur] == Free:
            rcur -= 1
        if lcur >= rcur:
            break
        disk[lcur] = disk[rcur]
        disk[rcur] = Free

    return sum(i * file for i, file in enumerate(disk) if file != Free)


def print_disk(disk):
    out = []
    for _ in disk:
        if _ == Free:
            out.append('.')
        else:
            out.append(str(_))
    print("".join(out))

def part2(s):
    return "TODO"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1))

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
