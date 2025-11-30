#!/usr/bin/env python3

from typing import NamedTuple
import re


ExampleInput1 = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

ExampleInput2 = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

ExampleInput3 = """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""

# box score = 100*x + y

class Point(NamedTuple):
  x: int
  y: int

  def __add__(self, other):
      return Point(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
      return Point(self.x - other.x, self.y - other.y)

  def __repr__(self):
      return f"({self.x}, {self.y})"

  def neighbors(self):
      return [self + d for d in DIRS]


N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)

DIRS = [N, E, S, W]
ARROWS = ['^', '>', 'v', '<']

def atod(c):
    return DIRS[ARROWS.index(c)]


class Grid:
    def __init__(self, s):
        self.grid = [list(_) for _ in s.splitlines()]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

        self.start = None
        for y in range(self.height):
            try:
                x = self.grid[y].index('@')
                self.start = Point(x, y)
                self[self.start] = '.'
                break
            except ValueError:
                pass
        if self.start == None:
            raise Exception("Did not find start")

    def points(self):
        return [Point(x, y) for x in range(self.width) for y in range(self.height)]

    def __getitem__(self, p):
        return self.grid[p.y][p.x]

    def __setitem__(self, p, v):
        self.grid[p.y][p.x] = v

    def move_box(self, src, d):
        dst = src + d
        match self[dst]:
            case '#':
                return False
            case 'O':
                if not self.move_box(dst, d):
                    return False
        self[src] = '.'
        self[dst] = 'O'
        return True

    def move_big_box(self, src, d, testonly=False):
        srcs = (src, src + E)
        dsts = (srcs[0] + d, srcs[1] + d)

        boxes = set()
        for p in dsts:
            if p in srcs:
                continue
            match self[p]:
                case '#':
                    return False
                case '[':
                    boxes.add(p)
                case ']':
                    boxes.add(p + W)

        if any(not self.move_big_box(p, d, testonly=True) for p in boxes):
            return False

        if testonly:
            return True

        for p in boxes:
            assert(self.move_big_box(p, d))
        for p in srcs:
            self[p] = '.'
        left, right = dsts
        self[left] = '['
        self[right] = ']'
        return True

    def dump(self):
        print("\n".join("".join(_) for _ in self.grid))

    def move_robot(self, pos, m):
        d = atod(m)
        dst = pos + d
        match self[dst]:
            case '#':
                return pos
            case '.':
                return dst
            case 'O':
                if self.move_box(dst, d):
                    return dst
            case '[':
                if self.move_big_box(dst, d):
                    return dst
            case ']':
                if self.move_big_box(dst + W, d):
                    return dst
        return pos

    def run(self, moves):
        pos = self.start
        for m in moves:
            pos = self.move_robot(pos, m)

    def score1(self):
        return sum(100 * p.y + p.x for p in self.points() if self[p] == 'O')

    def score2(self):
        return sum(100 * p.y + p.x for p in self.points() if self[p] == '[')


def parse(s):
    gridlines, movelines = s.split("\n\n")

    g = Grid(gridlines)
    moves = "".join(movelines.splitlines())
    return g, moves


def part1(s):
    g, moves = parse(s)
    g.run(moves)
    return g.score1()


def reformat_map(s):
    s = re.sub('#', '##', s)
    s = re.sub('O', '[]', s)
    s = re.sub('[.]', '..', s)
    s = re.sub('@', '@.', s)
    return s


def part2(s):
    g, moves = parse(reformat_map(s))
    g.run(moves)
    return g.score2()


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Small Example Part 1 (2028)")
    print(part1(ExampleInput2))

    print()
    print("Big Example Part 1 (10092)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (1514333)")
    print(part1(real_input()))

    print()
    print("Small Example Part 2 (618)")
    print(part2(ExampleInput3))

    print()
    print("Big Example Part 2 (9021)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1528453)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
