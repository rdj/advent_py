#!/usr/bin/env python3

from collections import defaultdict, deque
from functools import cache, cached_property
from itertools import combinations, permutations
from itertools import product
from math import prod
from typing import NamedTuple


ExampleInput1 = """\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""


# Problem says to look for at least 12 points in common between scanners to
# build the map. If there's 12 points, that's 12 choose 2 pairs of points.
REQUIRED_OVERLAP_POINTS = 12
REQUIRED_OVERLAP_PAIRS = REQUIRED_OVERLAP_POINTS * 11 // 2


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        x, y, z = other
        return Point(self.x + x, self.y + y, self.z + z)

    def __sub__(self, other):
        x, y, z = other
        return Point(self.x - x, self.y - y, self.z - z)

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    # Actual euclidean distance is the sqrt of this but there's no reason to
    # bother with that, we just want a number that represents the relationship
    # between two points that will be the same if we offset/orient them
    # differently.
    def distsq(self, other):
        d = self - other
        return d.x*d.x + d.y*d.y + d.z*d.z

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


class Rotations:
    @cache
    def all():
        return tuple(Rotations.build_rotators())

    def build_rotators():
        xysigns = tuple(product((-1, 1), (-1, 1)))
        for p in permutations(range(3)):
            fixed = sum(1 for i in range(3) if p[i] == i)
            parity = 1
            if fixed == 1:
                parity = -1
            for xysign in xysigns:
                signs = list(xysign) + [prod(xysign)*parity]
                yield Rotations.one_rotator(p, signs)


    def one_rotator(swaps, signs):
        return lambda xyz: Point(signs[0]*xyz[swaps[0]], signs[1]*xyz[swaps[1]], signs[2]*xyz[swaps[2]])


class Scanner:
    def __init__(self, readings):
        self.readings = readings
        self.mapped = None

    @cached_property
    def all_distances(self):
        return set(a.distsq(b) for a, b in combinations(self.readings, 2))

    @property
    def is_mapped(self):
        return self.mapped is not None

    def build_point_dists(self, points):
        pd = defaultdict(set)
        for a, b in combinations(points, 2):
            d = a.distsq(b)
            pd[a].add(d)
            pd[b].add(d)
        return {k: frozenset(v) for k, v in pd.items()}

    @cached_property
    def reading_dists(self):
        return self.build_point_dists(self.readings)

    @cached_property
    def mapped_dists(self):
        return self.build_point_dists(self.mapped)

    def filter_point_dists(self, pds, xdists):
        df = {}
        for k, v in pds.items():
            vfilt = v & xdists
            if len(vfilt) >= REQUIRED_OVERLAP_POINTS - 1:
                df[k] = vfilt
        return df

    def filter_reading_dists(self, xdists):
        return self.filter_point_dists(self.reading_dists, xdists)

    def filter_mapped_dists(self, xdists):
        return self.filter_point_dists(self.mapped_dists, xdists)

    def trymap(self, ref):
        xdistances = self.all_distances & ref.all_distances
        if len(xdistances) < REQUIRED_OVERLAP_PAIRS:
            return False

        ref_point_dists = ref.filter_mapped_dists(xdistances)
        my_point_dists = self.filter_reading_dists(xdistances)
        assert(len(ref_point_dists) == len(my_point_dists))

        my_lookup = {v: k for k, v in my_point_dists.items()}
        ref_points = []
        my_points = []
        for rp, d in ref_point_dists.items():
            ref_points.append(rp)
            my_points.append(my_lookup[d])

        for r in Rotations.all():
            offsets = {ref - r(my) for ref, my in zip(ref_points, my_points)}
            if len(offsets) > 1:
                continue
            offset = offsets.pop()
            self.mapped = tuple(r(p) + offset for p in self.readings)
            self.location = offset
            return True

        return False

    def use_as_reference(self):
        self.mapped = self.readings
        self.location = Point(0, 0, 0)


def parse(s):
    scanners = []
    secs = map(lambda x: x.splitlines(), s.split("\n\n"))

    for sec in secs:
        scanner = []
        for line in sec[1:]:
            scanner.append(Point(*map(int, line.split(","))))
        scanners.append(tuple(scanner))
    return tuple(scanners)


def common(s):
    scanners = [Scanner(readings) for readings in parse(s)]
    scanners[0].use_as_reference()

    cprod = deque(product(scanners, scanners))
    while not all(s.is_mapped for s in scanners):
        r, s = cprod.popleft()
        if r == s or s.is_mapped:
            continue
        if not r.is_mapped:
            cprod.append((r, s))
            continue

        s.trymap(r)
    return scanners


def part1(s):
    scanners = common(s)
    allpoints = {p for s in scanners for p in s.mapped}
    return len(allpoints)


def part2(s):
    scanners = common(s)
    return max(a.location.manhattan(b.location) for a, b in product(scanners, scanners))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (79)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (392)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (3621)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (13332)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
