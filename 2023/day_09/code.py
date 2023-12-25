#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

input = [list(map(int, line.split())) for line in input]

nexts = []

for line in input:
    stack = [line]
    while any(d := np.diff(stack[-1])):
        # print(f"{d=}")
        stack.append(d)

    delta = 0
    while stack:
        # print(f"{delta=}")
        delta += stack.pop()[-1]

    nexts.append(delta)

print(f"{sum(nexts)=}")

prevs = []

for line in input:
    stack = [line]
    while any(d := np.diff(stack[-1])):
        stack.append(d)

    prev = 0
    while stack:
        prev = stack.pop()[0] - prev

    prevs.append(prev)

print(f"{sum(prevs)=}")

pass
