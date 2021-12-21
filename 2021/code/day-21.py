#! /usr/bin/env python3

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

test = p1_position * kernel.transpose()

pass
