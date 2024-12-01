#!/usr/bin/env python3

import itertools as it
from multiprocessing import Pool

ExampleInput1 = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".strip()


def parse_ranges(lines):
    try:
        assert(':' in next(lines))
    except StopIteration:
        return None

    ranges = []

    for nums in lines:
        if nums == "":
            return ranges

        b, a, c = (int(_) for _ in nums.split())
        ranges.append([range(a, a+c), b])

    return ranges


def parse(s):
    lines = (_ for _ in s.splitlines());

    parsed = {}

    _, rest = next(lines).split(': ')
    parsed['seeds'] = [int(_) for _ in rest.split()]
    next(lines);

    parsed['maps'] = []
    while True:
        m = parse_ranges(lines)
        if not m:
            break
        parsed['maps'].append(m)

    return parsed


def do_map(n, mapper):
    for r, b in mapper:
        if n in r:
            return n - r[0] + b
    return n


def part1(s):
    d = parse(s)
    outputs = []

    for n in d['seeds']:
        for mapper in d['maps']:
            n = do_map(n, mapper)
        outputs.append(n)

    return min(outputs)


def part2(s):
    d = parse(s)

    inputs = [range(start, start+length) for start, length in it.batched(d['seeds'], n=2)]

    outputs = inputs

    for layer_num, mapping in enumerate(d['maps']):
        inputs = outputs
        outputs = []
        while len(inputs) > 0:
            inrange = inputs.pop()
            for matchrange, offset in mapping:
                overlap = range(max(inrange[0], matchrange[0]), min(inrange[-1], matchrange[-1]) + 1)
                if len(overlap) == 0:
                    continue

                outrange = range(overlap[0] - matchrange[0] + offset, overlap[-1] - matchrange[0] + offset + 1)
                assert(len(overlap) == len(outrange))
                outputs.append(outrange)

                before = range(inrange[0], overlap[0])
                if len(before) > 0:
                    inputs.append(before)

                after = range(overlap[-1] + 1, inrange[-1] + 1)
                if len(after) > 0:
                    inputs.append(after)

                assert(len(before) + len(overlap) + len(after) == len(inrange))
                inrange = None
                break
            if inrange:
                outputs.append(inrange)

    return min(r[0] for r in outputs)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read().strip()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (178159714)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (46)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (100165128)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
