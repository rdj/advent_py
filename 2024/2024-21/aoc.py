#!/usr/bin/env python3

from functools import cache, cached_property
from itertools import permutations


ExampleInput1 = """\
029A
980A
179A
456A
379A
"""

NumpadLayout = """\
789
456
123
-0A
"""

DirectionLayout = """\
-^A
<v>
"""

class EntryPad:
    def __init__(self, layout, layer):
        self.posmap = {}
        lines = layout.splitlines()
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                match lines[y][x]:
                    case '-':
                        self.gap = (x, y)
                    case c:
                        self.posmap[c] = (x, y)
        self.layer = layer

    @cache
    def shortest_deepest_path(self, src, dst):
        inputs = []
        x0, y0 = src
        x1, y1 = dst
        dx = x1 - x0
        dy = y1 - y0

        xdir = '>'
        if dx < 0:
            dx = -dx
            xdir = '<'
        inputs += [xdir] * dx

        ydir = 'v'
        if dy < 0:
            dy = -dy
            ydir = '^'
        inputs += [ydir] * dy

        paths = set(permutations(inputs))
        for p in list(paths):
            x, y = src
            for d in p:
                match d:
                    case '>':
                        x += 1
                    case '<':
                        x -= 1
                    case 'v':
                        y += 1
                    case '^':
                        y -= 1
                if (x, y) == self.gap:
                    paths.remove(p)
                    break

        if self.next_layer:
            return min(self.next_layer.shortest_inputlen("".join(p) + "A") for p in paths)
        else:
            return min(map(len, paths)) + 1

    def shortest_inputlen(self, code):
        inputs = 0
        src = self.posmap['A']
        for c in code:
            dst = self.posmap[c]
            inputs += self.shortest_deepest_path(src, dst)
            src = dst
        return inputs

    @cached_property
    def next_layer(self):
        if self.layer == 0:
            return None
        return EntryPad(DirectionLayout, self.layer - 1)


def compute_complexity(s, layers):
    n = EntryPad(NumpadLayout, layers)
    return sum(n.shortest_inputlen(code) * int(code[:-1]) for code in s.splitlines())


def part1(s):
    return compute_complexity(s, 2)


def part2(s):
    return compute_complexity(s, 25)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (126384)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (278748)")
    print(part1(real_input()))

    print()
    print("Part 2 (337744744231414)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
