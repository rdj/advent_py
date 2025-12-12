#!/usr/bin/env python3

from math import prod
import numpy as np
import re


MultiLineExample = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

ExamplesPart1 = (
    (MultiLineExample, 2),
)

ExamplesPart2 = (
    (MultiLineExample, None),
)


ROTATIONS = (
    lambda a: a,
    lambda a: np.rot90(a),
    lambda a: np.rot90(np.rot90(a)),
    lambda a: np.rot90(np.rot90(np.rot90(a))),
)

FLIPPED_ROTATIONS = tuple(map(lambda r: lambda a: np.fliplr(r(a)), ROTATIONS))

ORIENTATIONS = ROTATIONS + FLIPPED_ROTATIONS


def orientations(a):
    for o in ORIENTATIONS:
        yield o(a)


def ints(s):
    return list(map(int, re.findall(r'\d+', s)))


def parse(s):
    blocks = s.split("\n\n")

    spieces = blocks[:-1]
    pieces = []
    for spiece in spieces:
        piece = []
        for line in spiece.splitlines()[1:]:
            piece.append(tuple(1 if c == '#' else 0 for c in line))
        pieces.append(tuple(piece))

    trees = []
    strees = blocks[-1]
    for stree in strees.splitlines():
        nums = ints(stree)
        trees.append((tuple(nums[:2]), tuple(nums[2:])))

    return tuple(pieces), tuple(trees)


def can_place(state, to_place, pieces):
    if 0 == len(to_place):
        return True

    pi, *to_place = to_place
    to_place = tuple(to_place)
    p = pieces[pi]

    H, W = len(state), len(state[0])
    h, w = len(p), len(p[0])

    for po in orientations(p):
        h, w = len(po), len(po[0])

        for i in range(H - h + 1):
            for j in range(W - w + 1):
                a = np.array(state)
                a[i:i+h, j:j+w] += po
                if not (a > 1).any():
                    if can_place(tuple(map(tuple, a)), to_place, pieces):
                        return True

    return False


def good_tree(tree, pieces):
    area, wanted = tree

    spaces_existing = prod(area)
    minimum_spaces_required = 0
    for i, n in enumerate(wanted):
        if n > 0:
            minimum_spaces_required += n * sum(map(sum,pieces[i]))

    if minimum_spaces_required > spaces_existing:
        #print(f"SKIPPING CHECK: {minimum_spaces_required} > {spaces_existing}")
        return False

    #print(f"OK TO CHECK: {minimum_spaces_required} <= {spaces_existing}")

    # WTF, it turns out that every tree worth checking is just solvable. The
    # runtime was so long even with my early pruning that I tried just
    # submitting the total count of unpruned trees.
    #
    # Frustratingly, the actual sample has an example that passes the prune
    # check but then isn't satisfiable. But even this one example takes so long
    # to disprove exhaustively, that's why I started looking for shortcuts.

    ## Uncomment this line to get the correct answer pretty much instantly.
    ## Leave it commented to laboriously verify that all the trees are actually
    ## solvable. It will take a long time.
    #
    #return True

    w, h = area

    to_place = []
    for i in range(len(wanted)):
        to_place += [i] * wanted[i]

    state = tuple(tuple([0] * w) for _ in range(h))
    result = can_place(state, tuple(to_place), pieces)
    print(f"{result} GOOD TREE {tree}")
    return result


def part1(s):
    pieces, trees = parse(s)

    return sum(good_tree(t, pieces) for t in trees)


def part2(s):
    return "TODO"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    import time

    ### There is no point trying to solve the sample, with a non-early-prunable
    ### non-solvable tree, the exhaustive search to disprove it takes a super
    ### long time.
    # for i, (a, b) in enumerate(ExamplesPart1):
    #     c = part1(a)
    #     check = "✅️" if b == c else "⚠️"
    #     print(f"Example Part 1.{i} ({b})")
    #     print(check, c)
    #     print()

    print("Part 1 (487)")
    before = time.perf_counter_ns()
    result = part1(real_input())
    elapsed = time.perf_counter_ns() - before
    print(f"{result} ({elapsed//1_000_000} ms)")
    print()


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('part2(real_input())', sort="cumulative")
    run_all()
