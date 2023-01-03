#!/usr/bin/env python3

from collections import deque
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
            m.group("name"),
            int(m.group("rate")),
            m.group("tunnels").split(", ")
        )
        valves[v.name] = v

    return valves


def shortest_paths(valves):
    G = nx.Graph()
    for v in valves.values():
        for t in v.tunnels:
            G.add_edge(v.name, t)

    return dict(nx.all_pairs_shortest_path_length(G))


class WorkItem(NamedTuple):
    time: int
    pos: str
    flow: int
    opened: list

    def best_key(self):
        return (self.pos, self.opened)


def best_flow(valves, time_limit):
    SRC = "AA"

    costs = shortest_paths(valves)
    to_open = [v.name for v in valves.values() if v.rate > 0]
    best = {}

    q = deque()
    q.append(WorkItem(time=0, pos=SRC, flow=0, opened=()))

    while len(q) > 0:
        cur = q.popleft()

        if cur.flow < best.get(cur.best_key(), 0):
            continue

        for v in to_open:
            if v in cur.opened:
                continue

            t = cur.time + costs[cur.pos][v] + 1
            f = cur.flow + valves[v].rate * (time_limit - t)
            o = list(cur.opened)
            o.append(v)
            o.sort()
            o = tuple(o)

            w = WorkItem(time=t, pos=v, flow=f, opened=o)
            key = w.best_key()
            if w.flow < best.get(key, 0):
                continue
            best[key] = w.flow

            q.append(w)

    return max(best.values())


def part1(s):
    valves = parse(s)
    return best_flow(valves, 30)


def part2(s):
    return "TODO"


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
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
