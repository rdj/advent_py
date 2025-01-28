#!/usr/bin/env python3


from collections import defaultdict, Counter
from math import prod
import numpy as np
import re


ExampleInput1 = """\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

# I don't think there's a way to match the same length of arbitrary padding on
# each line, so just make enough regexes to cover all line lengths. I wrote a
# version that just used numpy to find matches, but it took about 30% longer
# compared this this silly set of regexes.
DARGON = "^..................1.*\n^1....11....11....111.*\n^.1..1..1..1..1..1"
DARGONS = [re.compile(re.sub(r"\^", "^" + "." * r, DARGON), flags=re.MULTILINE) for r in range(100-20)]
DARGON_SIZE = len(re.findall("1", DARGON))


ROTATIONS = (
    lambda a: a,
    lambda a: np.rot90(a),
    lambda a: np.rot90(np.rot90(a)),
    lambda a: np.rot90(np.rot90(np.rot90(a))),
)

FLIPPED_ROTATIONS = tuple(map(lambda r: lambda a: np.fliplr(r(a)), ROTATIONS))

ORIENTATIONS = ROTATIONS + FLIPPED_ROTATIONS


def parse(s):
    s = s.translate(s.maketrans(".#", "01"))
    blocks = {}
    edges = defaultdict(list)

    for block in s.split("\n\n"):
        lines = block.splitlines()
        blockid = int(lines[0].split()[-1][:-1])
        a = np.array([list(line) for line in lines[1:]], np.uint8)
        blocks[blockid] = [o(a) for o in ORIENTATIONS]
        for a in blocks[blockid]:
            edges[tuple(a[0])].append(blockid)

    return blocks, edges


def find_corners(edges):
    unmatched_edges = Counter([ids[0] for _, ids in edges.items() if len(ids) == 1])
    return [bid for bid, n in unmatched_edges.items() if n == 4]


def part1(s):
    _, edges = parse(s)
    return prod(find_corners(edges))


def solve(blocks, edges):
    dim = int(len(blocks)**0.5)
    img = np.full((dim, dim), None)

    # Choose a random corner and put it in the top-left in a correct
    # orientation. (Note that there are 2 valid orientations.)
    start = find_corners(edges)[0]
    for i, a in enumerate(blocks[start]):
        topmatches = edges[tuple(a[0])]
        leftmatches = edges[tuple(a[:, 0])]
        if len(topmatches) == 1 and len(leftmatches) == 1:
            img[0][0] = (start, i)
            break

    def _match(imgji, src_edge, dst_edge):
        srcb, srco = imgji
        src = blocks[srcb][srco]
        e = tuple(src[src_edge])
        dstb = [b for b in edges[e] if b != srcb][0]
        for k, a in enumerate(blocks[dstb]):
            if e == tuple(a[dst_edge]):
                return (dstb, k)

    def match_above(imgji):
        return _match(imgji, (-1, slice(None)), (0, slice(None)))

    def match_left(imgji):
        return _match(imgji, (slice(None), -1), (slice(None), 0))

    for j in range(dim):
        for i in range(dim):
            if (i,j) == (0,0):
                continue
            if i == 0:
                img[j][i] = match_above(img[j-1, i])
            else:
                img[j][i] = match_left(img[j, i-1])

    return img


def assemble(blocks, edges):
    sol = solve(blocks, edges)
    nblocks = len(sol)
    nchars = len(blocks[sol[0][0][0]])
    dim = nblocks * nchars
    img = np.empty((dim, dim), np.uint8)

    for j in range(nblocks):
        for i in range(nblocks):
            b, o = sol[j][i]
            a = blocks[b][o]
            img[j*nchars:(j+1)*nchars, i*nchars:(i+1)*nchars] = a[1:-1, 1:-1]

    return img


def part2(s):
    img = assemble(*parse(s))

    pounds = 0
    found = 0
    for i, o in enumerate(ORIENTATIONS):
        a = o(img)
        s = "\n".join(["".join(map(lambda c: str(int(c)), line)) for line in a])
        found = sum(len(re.findall(d, s)) for d in DARGONS)
        if found:
            pounds = int(a.sum())
            break

    return pounds - DARGON_SIZE*found


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (20899048083289)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (8272903687921)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (273)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (2304)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
