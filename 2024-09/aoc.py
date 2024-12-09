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
    s = s.splitlines()[0]
    diskmap = []

    file = 0
    space = False
    for n in s:
        n = int(n)
        if space:
            diskmap.append((Free, n))
        else:
            diskmap.append((file, n))
            file += 1
        space = not space

    maxfile = file - 1

    for fid in range(maxfile, -1, -1):
        #print_diskmap(diskmap)
        start_index = None
        size = None
        for i in range(len(diskmap)):
            if diskmap[i][0] == fid:
                start_index = i
                size = diskmap[i][1]
                break

        dest_index = None
        dest_size = None
        for i in range(start_index):
            if diskmap[i][0] != Free:
                continue
            if diskmap[i][1] >= size:
                dest_index = i
                dest_size = diskmap[i][1]
                break

        if dest_index != None:
            diskmap = move_file(diskmap, start_index, dest_index)

    cur = 0
    total = 0
    for file, size in diskmap:
        if file != Free:
            total += sum(file*n for n in range(cur, cur+size))
        cur += size

    return total

def move_file(diskmap, start, dest):
    file, size = diskmap[start]

    newmap = diskmap[:dest]
    freelen = 0
    for i, e in enumerate(diskmap):
        if i < dest:
            continue

        if i == start:
            freelen += size
            continue

        if i == dest:
            assert(freelen == 0)
            newmap.append((file, size))
            freelen = diskmap[dest][1] - size
            continue

        f, s = e
        if f == Free:
            freelen += s
            continue

        if freelen > 0:
            newmap.append((Free, freelen))
            freelen = 0
        newmap.append(e)

    if freelen > 0:
        newmap.append((Free, freelen))

    return newmap


def print_diskmap(diskmap):
    s = []
    for (n, size) in diskmap:
        c = str(n)
        if n == Free:
            c = '.'
        s.append(c * size)
    print("".join(s))

def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (1928)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (6154342787400)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2858)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (6183632723350)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
