#!/usr/bin/env python3


ExampleInput1 = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

N = (0, -1)
E = (1, 0)
S = (0, 1)
W = (-1, 0)

DIRS = [N, E, S, W]
FACING = ['^', '>', 'v', '<']


class Grid:
    def __init__(self, s):
        self.tiles = [list('~' + _ + '~') for _ in s.splitlines()]
        outside = '~' * len(self.tiles[0])
        self.tiles = [outside] + self.tiles + [outside]

        self.height = len(self.tiles)
        self.width = len(self.tiles[0])
        self.start = self.find_start()

    def points(self):
        return ((x, y) for x in range(self.width) for y in range(self.height))

    def find_start(self):
        for x,y in self.points():
            t = self.tiles[y][x]
            if t in FACING:
                return (x, y), FACING.index(t)
        raise Exception()

    def find_path(self):
        p, d = self.start
        visited = set()
        while True:
            visited.add((p, d))
            dx, dy = DIRS[d]
            dst = (p[0] + dx, p[1] + dy)
            if (dst, d) in visited:
                return None
            t = self.tiles[dst[1]][dst[0]]
            if t == '~':
                break
            if t == '#':
                d = turn90(d)
                continue
            p = dst

        return visited


def turn90(d):
    return (d + 1) % len(DIRS)


def part1(s):
    g = Grid(s)
    path = g.find_path()
    return len(set(_[0] for _ in path))


def part2(s):
    g = Grid(s)

    path = g.find_path()
    uniqs = set(_[0] for _ in path)

    loops = 0
    for x, y in uniqs:
        if g.tiles[y][x] == '.':
            g.tiles[y][x] = '#'
            if g.find_path() == None:
                loops += 1
            g.tiles[y][x] = '.'

    return loops


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (41)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (5212)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (6)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1767)")
    print(part2(real_input()))


if __name__ == "__main__":
    #cProfile.run('run_all()', sort='cumulative')
    run_all()
