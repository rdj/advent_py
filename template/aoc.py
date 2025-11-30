#!/usr/bin/env python3

## Things I used in previous years

# from colors import color  ## pip install py-colors

# from bitstring import Bits, BitStream
# from collections import Counter
# from collections import defaultdict
# from collections import deque
# from copy import deepcopy
# from dataclasses import dataclass, astuple, replace
# from enum import Enum, IntEnum, auto
# from fractions import Fraction
# from functools import cache, cached_property
# from functools import cmp_to_key
# from functools import lru_cache
# from functools import partial
# from functools import reduce
# from heapq import heappush, heappop
# from itertools import combinations
# from itertools import count
# from itertools import cycle
# from itertools import groupby
# from itertools import islice
# from itertools import pairwise
# from itertools import permutations
# from itertools import product    ## Cartesian product
# from math import log
# from math import prod
# from math import sqrt
# from more_itertools import batched
# from more_itertools import chunked
# from more_itertools import ilen
# from more_itertools import sliding_window
# from multiprocessing import Pool
# from numpy import transpose
# from pathlib import Path
# #from scipy.signal import convolve2d ## pypy3 unsupported
# from typing import NamedTuple
# import _md5
# import cProfile
# import functools as ft
# import itertools as it
# import json
# import math
# import networkx as nx
# import numpy as np
# import operator as op
# import pygraphviz as pgv
# import re
# import regex # supports overlapped matches, recursive subpatterns (?<foo>...(?&foo)*...)
# import sympy
# import z3 # pip install z3-solver


MultiLineExample = """\
"""

ExamplesPart1 = (
    # ("input", output),
)

ExamplesPart2 = (
)


def part1(s):
    return "TODO"


def part2(s):
    return "TODO"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 ()")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 ()")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
