#!/usr/bin/env python3

from collections import deque
from heapq import heappush, heappop
import re
from typing import NamedTuple

import networkx as nx


ExampleInput1 = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


VALVE_PATTERN = re.compile(
    r"Valve (?P<name>\S+) "
    r"has flow rate=(?P<rate>\d+); "
    r"tunnels? leads? to valves? (?P<tunnels>.*)"
)


class Valve:
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = rate
        self.tunnels = tunnels

    def __repr__(self):
        return f"Valve({self.name}, {self.rate}, {self.tunnels})"


def parse(s):
    valves = {}

    for line in s.splitlines():
        m = VALVE_PATTERN.match(line)
        assert m, line
        v = Valve(
            m["name"],
            int(m["rate"]),
            m["tunnels"].split(", ")
        )
        valves[v.name] = v

    return valves


# When I solved this problem in Go, I implemented Floyd-Warshall myself, but
# since I'd already done that I decided there was more value in learning how
# to use networkx in python.
def shortest_paths(valves):
    G = nx.Graph()
    for v in valves.values():
        for t in v.tunnels:
            G.add_edge(v.name, t)

    return dict(nx.all_pairs_shortest_path_length(G))


class Worker(NamedTuple):
    time: int
    pos: str


class WorkItem(NamedTuple):
    workers: tuple
    flow: int
    opened: int

    def best_key(self):
        return (self.workers[0].pos, self.workers[1].pos, self.opened)


def best_flow(valves, time_limit, friend=False):
    SRC = "AA"

    costs = shortest_paths(valves)
    to_open = [v.name for v in valves.values() if v.rate > 0]
    best = {}
    best_overall = 0

    def max_possible_flow(w):
        """Heuristic function for pruning and A-star priority. Computes
        an overestimate of the max possible flow by just assuming all
        the rest of the valves magically open all at once right now."""
        t = max(w.workers[0].time, w.workers[1].time)
        vf = 0
        for i, v in enumerate(to_open):
            if not w.opened & 1 << i:
                vf += valves[v].rate
        vf *= time_limit - t
        return w.flow + vf

    q = []
    heappush(q, (0, WorkItem((Worker(0, SRC), Worker(0, SRC)), flow=0, opened=0)))

    while len(q) > 0:
        curmaxf, cur = heappop(q)

        if -curmaxf < best_overall:
            continue

        wi = 0
        if friend and cur.workers[1].time < cur.workers[0].time:
            wi = 1

        for i, v in enumerate(to_open):
            flag = 1 << i
            if cur.opened & flag:
                continue

            t = cur.workers[wi].time + costs[cur.workers[wi].pos][v] + 1
            f = cur.flow + valves[v].rate * (time_limit - t)
            o = cur.opened | flag

            workers = list(cur.workers)
            workers[wi] = Worker(t, v)

            w = WorkItem(workers=workers, flow=f, opened=o)

            maxf = max_possible_flow(w)
            if maxf < best_overall:
                continue

            key = w.best_key()
            if w.flow < best.get(key, 0):
                continue
            best[key] = w.flow

            best_overall = max(best_overall, w.flow)

            heappush(q, (-maxf, w))

    return best_overall


def part1(s):
    valves = parse(s)
    return best_flow(valves, 30)


def part2(s):
    valves = parse(s)
    return best_flow(valves, 26, friend=True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (1651)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (1647)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (1707)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (2169)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
