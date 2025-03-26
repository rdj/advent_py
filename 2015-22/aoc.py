#!/usr/bin/env pypy3

import re
from dataclasses import dataclass, astuple, replace
from heapq import heappush, heappop


@dataclass
class GameState:
    mana_spent: int = 0
    boss_hp: int = 0
    player_mana: int = 500
    player_hp: int = 50
    shield_timer: int = 0
    poison_timer: int = 0
    recharge_timer: int = 0
    boss_dmg: int = 0
    hard_mode: bool = False


    def has_won(self):
        return self.player_hp > 0 and self.boss_hp <= 0


    def is_valid(self):
        if self.player_mana < 0 or self.player_hp <= 0:
            return False
        if self.player_mana < 53 and self.recharge_timer == 0 and self.boss_hp > 0:
            return False
        return True


    def boss_turn(self):
        if self.boss_hp > 0:
            armor = self.tick_effects()
            self.player_hp -= max(1, self.boss_dmg - armor)


    def tick_effects(self):
        armor = 0
        if self.shield_timer > 0:
            self.shield_timer -= 1
            armor = 7
        if self.poison_timer > 0:
            self.poison_timer -= 1
            self.boss_hp -= 3
        if self.recharge_timer > 0:
            self.recharge_timer -= 1
            self.player_mana += 101
        return armor


    def cast(self, m, **rest):
        return replace(
            self,
            mana_spent=self.mana_spent + m,
            player_mana=self.player_mana - m,
            **rest
        )


    def casts(self):
        m = self.player_mana
        if m > 53:
            yield self.cast(53, boss_hp=self.boss_hp-4)
        if m > 73:
            yield self.cast(73, player_hp=self.player_hp+2, boss_hp=self.boss_hp-2)
        if m > 113 and self.shield_timer == 0:
            yield self.cast(113, shield_timer=6)
        if m > 173 and self.poison_timer == 0:
            yield self.cast(173, poison_timer=6)
        if m > 229 and self.recharge_timer == 0:
            yield self.cast(229, recharge_timer=5)


    def next(self):
        if self.hard_mode:
            self.player_hp -= 1
            if not self.is_valid():
                return
        self.tick_effects()
        if not self.is_valid():
            return
        for n in self.casts():
            n.boss_turn()
            if n.is_valid():
                yield n


def parse(s):
    a, b = tuple(int(x) for x in re.findall(r"\d+", s))
    return { 'boss_hp': a, 'boss_dmg': b }


def run(g):
    q = [astuple(g)]
    visited = set()

    while q:
        g = heappop(q)

        if g in visited:
            continue
        visited.add(g)

        g = GameState(*g)
        if g.has_won():
            return g.mana_spent

        for n in g.next():
            heappush(q, astuple(n))

    return "NO SOLUTION FOUND"


def part1(s):
    return run(GameState(**parse(s)))


def part2(s):
    d = parse(s)
    d['hard_mode'] = True
    return run(GameState(**d))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (953)")
    print(part1(real_input()))
    print()

    print("Part 2 (1289)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
