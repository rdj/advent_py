#!/usr/bin/env python3

ExampleInput1 = '''\
30373
25512
65332
33549
35390
'''

class Grid:
    def __init__(self, rows):
        rows = [
            [int(_) for _ in row]
            for row in rows
        ]
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])
        self.cols = list(zip(*self.rows, strict=True))

    def is_visible(self, x, y):
        if self.on_edge(x, y):
            return True
        height = self.rows[y][x]
        for r in self.rays(x, y):
            if max(r) < height:
                return True

    def on_edge(self, x, y):
        return (
            x == 0 or
            y == 0 or
            x == self.width - 1 or
            y == self.width - 1
        )

    def rays(self, x, y):
        return (
            reversed(self.rows[y][:x]), # west
            self.rows[y][x+1:],         # east
            reversed(self.cols[x][:y]), # north
            self.cols[x][y+1:],         # south
        )

    def score(self, x, y):
        height = self.rows[y][x]
        score = 1
        for r in self.rays(x, y):
            rs = 0
            for n in r:
                rs += 1
                if n >= height:
                    break
            score *= rs
        return score

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

def part1(input):
    g = Grid(input.splitlines())
    vis = 0
    for y in range(0, g.height):
        for x in range(0, g.width):
            if g.is_visible(x, y):
                vis += 1
    return vis

def part2(input):
    g = Grid(input.splitlines())
    best = 0
    for y in range(0, g.height):
        for x in range(0, g.width):
            best = max(best, g.score(x, y))
    return best

print('Example Part 1 (want 21)')
print(part1(ExampleInput1))

print()
print('Part 1')
print(part1(realinput()))

print()
print('Example Part 2 (want 8)')
print(part2(ExampleInput1))

print()
print('Part 2')
print(part2(realinput()))
