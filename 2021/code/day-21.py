#! /usr/bin/env python3

from collections import namedtuple, defaultdict
import numpy as np

"""
Player 1 starting position: 9
Player 2 starting position: 3
"""

p1_position = 8
p2_position = 2

p1_score = 0
p2_score = 0


class Die:
    def __init__(self):
        self.value = 0
        self.rolls = 0
        return

    def roll(self):
        self.rolls += 1
        retval = self.value + 1
        self.value += 1
        self.value %= 100
        return retval


d = Die()
while True:
    rolls = d.roll() + d.roll() + d.roll()
    p1_position += rolls
    p1_position %= 10
    p1_score += p1_position + 1
    if p1_score >= 1000:
        break
    rolls = d.roll() + d.roll() + d.roll()
    p2_position += rolls
    p2_position %= 10
    p2_score += p2_position + 1
    if p2_score >= 1000:
        break

loser = min(p1_score, p2_score)
print(f"{loser*d.rolls=}")

kernel = np.array([0, 0, 0, 1, 3, 6, 7, 6, 3, 1], dtype=np.uint64)

p1_position = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0], dtype=np.uint64)
p2_position = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint64)

Roll = namedtuple("Roll", ["total", "ways"])

rolls = [
    Roll(3, 1),     # 1+1+1
    Roll(4, 3),     # 1+1+2, 1+2+1, 2+1+1
    Roll(5, 6),     # 1+1+3, 1+2+2, 1+3+1, 2+1+2, 2+2+1, 3+1+1
    Roll(6, 7),     # 1+2+3, 1+3+2, 2+1+3, 2+2+2, 2+3+1, 3+1+2, 3+2+1
    Roll(7, 6),     # 1+3+3, 2+2+3, 2+3+2, 3+1+3, 3+2+2, 3+3+1
    Roll(8, 3),     # 2+3+3, 3+2+3, 3+3+2
    Roll(9, 1)      # 3+3+3
]


def next_state(old_state, other):
    new_state = [defaultdict(int) for _ in range(10)]
    wins = 0
    for position in range(10):
        for score, ways in old_state[position].items():
            for roll in rolls:
                new_position = (position + roll.total) % 10
                new_score = score + (new_position + 1)
                new_ways = ways * roll.ways
                if new_score >= 21:
                    wins += new_ways * other
                else:
                    new_state[new_position][new_score] += new_ways

    return new_state, wins


def total_ways(state):

    total = 0
    for position in state:
        for ways in position.values():
            total += ways

    return total


p1 = [[{} for _ in range(10)]]
p1[0][8] = {0: 1}   # start = 9
# p1[0][3] = {0: 1}   # test start = 4

p2 = [[{} for _ in range(10)]]
p2[0][2] = {0: 1}   # start = 3
# p2[0][7] = {0: 1}   # test start = 8

p1_wins = 0
p2_wins = 0

while True:
    state = p1[-1]
    new_state, additional_wins = next_state(state, other=total_ways(p2[-1]))
    p1.append(new_state)
    p1_wins += additional_wins
    if not any(new_state):
        break

    state = p2[-1]
    new_state, additional_wins = next_state(state, other=total_ways(p1[-1]))
    p2.append(new_state)
    p2_wins += additional_wins
    if not any(new_state):
        break


print(f"     {p1_wins:30},         {p2_wins:30}")
print(f"c.f. {444356092776315:30} and      {341960390180808:30}")

pass
