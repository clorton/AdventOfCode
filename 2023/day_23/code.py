#! /usr/bin/env python3

from collections import defaultdict, deque, namedtuple
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "example.txt"

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

HASH = ord("#")
DOT = ord(".")
RIGHT = ord(">")
DOWN = ord("v")

Cell = namedtuple("Cell", ["y", "x"])

input = np.array([list(map(ord, line)) for line in input])
visited = np.zeros_like(input, dtype=np.uint32)
start = Cell(0,1)
consider = deque([start])
visited[start] = 1
while consider:
    test = consider.popleft()
    length = visited[test]
    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        y = test.y + dy
        x = test.x + dx
        if y < 0 or y >= input.shape[0] or x < 0 or x >= input.shape[1]:
            continue
        if input[y, x] == HASH:
            continue
        if visited[y, x] >= (length + 1):
            continue
        if input[y, x] == DOT:
            # in bounds - check
            # not a forest - check
            # length < length + 1
            visited[y, x] = length + 1
            consider.append(Cell(y, x))
        elif input[y, x] == RIGHT:
            if dx == -1:
                continue
            x += 1
            if visited[y, x] >= (length + 2):
                continue
            visited[y, x] = length + 2
            consider.append(Cell(y, x))
        elif input[y, x] == DOWN:
            if dy == -1:
                continue
            y += 1
            if visited[y, x] >= (length + 2):
                continue
            visited[y, x] = length + 2
            consider.append(Cell(y, x))
        else:
            raise ValueError(f"Unknown input: {input[y, x]=}")

pass
