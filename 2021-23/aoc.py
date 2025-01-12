#!/usr/bin/env pypy3

from collections import defaultdict
from heapq import heappush, heappop
from typing import NamedTuple


ExampleInput1 = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
#123456789AB
#  ^ ^ ^ ^


NROOMS = 4
X0ROOMS = 3
WROOM = 2
YROOMS = 2

YHALLWAY = 1
WHALLWAY = 11

EMPTYING = -1
DONE = 0
FILLING = 1


def manhattan(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return abs(x1 - x0) + abs(y1 - y0)


def parse(s):
    d = defaultdict(list)
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c != '.' and c != '#':
                d[c].append((x, y,))

    return tuple(d['A'] + d['B'] + d['C'] + d['D'])


def is_complete(s):
    pods = s[1]
    pertype = len(pods) // NROOMS

    for i, (x, y) in enumerate(pods):
        xf = X0ROOMS + WROOM*(i//pertype)
        if x != xf:
            return False
    return True


def scan(inpods):
    pertype = len(inpods) // NROOMS

    hallway = [True] + [False] * WHALLWAY + [True]

    roomidx = [None] * NROOMS * pertype
    for i,p in enumerate(inpods):
        x,y = p
        if y == YHALLWAY:
            hallway[x] = True
        else:
            roomidx[(x//WROOM - 1)*pertype + y - YROOMS] = i

    rooms = []
    for i in range(NROOMS):
        hasbad = False
        ytop = None
        for j in range(0, pertype):
            ri = pertype * i + pertype - 1 - j
            y = 1 + pertype - j

            if roomidx[ri] is None:
                break

            ytop = y
            if pertype*i <= roomidx[ri] < pertype*(i+1):
                pass
            else:
                hasbad = True

        if hasbad:
            rooms.append((EMPTYING, ytop))
        elif ytop == YROOMS:
            rooms.append((DONE, 0))
        else:
            rooms.append((FILLING, y))

    return hallway, rooms

COSTS = [1, 10, 100, 1000]

def next_states(s):
    incost, inpods = s
    pertype = len(inpods) // NROOMS
    hallway, rooms = scan(inpods)

    #print(inpods)
    #print(hallway)
    #print(rooms)

    for i, p in enumerate(inpods):
        x,y = p
        base_cost = COSTS[i//pertype]

        if y == YHALLWAY: # in hallway, must move to room
            ri = i//pertype
            rs, yf = rooms[ri]

            if rs != FILLING:
                #print(f"Pod {i} must stay in hallway; room not ready")
                continue
            dst = (ri * WROOM + X0ROOMS, yf)
            steps = manhattan(p, dst)
            blocked = False
            for j in range(min(x, dst[0]), max(x, dst[0]) + 1):
                if j != x and hallway[j]:
                    blocked = True
                    break
            if not blocked:
                #print(f"Pod {i} moving from hallway {p} to room {ri} {dst} at cost {steps} * {base_cost}")
                yield (incost + steps * base_cost, inpods[:i] + (dst,) + inpods[i+1:])
            else:
                #print(f"Pod {i} blocked from hallway {p} to room {ri} {dst}")
                pass
        else: # in room, must move to hallway
            ri = (x - X0ROOMS)//WROOM
            rs, yf = rooms[ri]

            if rs != EMPTYING or yf != y:
                #print(f"Pod {i} must stay in room {ri}, {rs} {yf}")
                continue

            xmin = x
            while not hallway[xmin]:
                xmin -= 1
            xmax = x
            while not hallway[xmax]:
                xmax += 1

            for xh in range(xmin + 1, xmax):
                if (xh % 2 == 1 and 3 <= xh <= 9):
                    # Can't move into the space above a room
                    continue
                dst = (xh, 1)
                steps = manhattan(p, dst)
                #print(f"Pod {i} moving from room {ri} {p} to hallway {dst} at cost {steps} * {base_cost}")
                yield (incost + steps * base_cost, inpods[:i] + (dst,) + inpods[i+1:])


def part1(s):
    visited = set()
    best_cost = defaultdict(lambda: 1<<16)

    q = []
    heappush(q, (0, parse(s)))

    while q:
        s = heappop(q)

        if is_complete(s):
            return s[0]

        if s[1] in visited:
            continue
        visited.add(s[1])

        for n in next_states(s):
            if n[0] < best_cost[n[1]]:
                best_cost[n[1]] = n[0]
                heappush(q, n)

    return "No solution found"


PART2_LINES = """\
  #D#C#B#A#
  #D#B#A#C#
"""

def part2(s):
    lines = s.splitlines()
    lines = lines[:-2] + PART2_LINES.splitlines() + lines[-2:]
    s = "\n".join(lines)
    return part1(s)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (12521)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (14346)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (44169)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (48984)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
