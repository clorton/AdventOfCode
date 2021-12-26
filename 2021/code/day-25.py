#! /usr/bin/env python3

from pathlib import Path

import numpy as np

with Path("../inputs/25.txt").open("r") as handle:
    lines = list([list(map(ord, list(line.strip()))) for line in handle.readlines()])

splines = [list(map(ord, list(line))) for line in [
    "v...>>.vv>",
    ".vv>>.vv..",
    ">>.>v>...v",
    ">>v>>.>.v.",
    "v>v.vv.v..",
    ">.>>..v...",
    ".vv..>.>v.",
    "v.v..>>v.v",
    "....v..v.>"
    ]]

SPACE = ord(".")
RIGHT = ord(">")
DOWN = ord("v")

state = np.array(lines, dtype=np.uint32)


def print_state(state):
    height = state.shape[0]
    for y in range(height):
        print("".join(map(chr, state[y, :])))
    print()
    return


def step(state):
    prev = np.array(state, dtype=state.dtype)
    height, width = state.shape
    rights = np.nonzero((state == RIGHT) & (np.roll(state, -1, 1) == SPACE))
    for y, x in zip(*rights):
        state[y, x] = SPACE
        state[y, (x+1) % width] = RIGHT

    downs = np.nonzero((state == DOWN) & (np.roll(state, -1, 0) == SPACE))
    for y, x in zip(*downs):
        state[y, x] = SPACE
        state[(y+1) % height, x] = DOWN

    return np.array_equal(state, prev)


iteration = 0
while True:
    iteration += 1
    if iteration % 100 == 0:
        print(f"{iteration=}")
    if step(state):
        break

print(f"State unchanged after {iteration} iterations.")

pass
