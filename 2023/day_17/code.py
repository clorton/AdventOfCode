#! /usr/bin/env python3

from collections import defaultdict, namedtuple
import heapq
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "example.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

city = np.array([list(map(int, list(line))) for line in input])

Position = namedtuple("Position", ["x", "y"])
Velocity = namedtuple("Velocity", ["dx", "dy"])
State = namedtuple("State", ["position", "history", "loss"])

INITIAL = Velocity(0, 0)
UP = Velocity(1, 0)
DOWN = Velocity(-1, 0)
LEFT = Velocity(0, -1)
RIGHT = Velocity(0, 1)

best = [[{} for _ in range(city.shape[1])] for _ in range(city.shape[0])]

loss = 0
position = Position(0, 0)
consecutive = {UP: 0, DOWN: 0, LEFT: 0, RIGHT: 0}
best[0][0] = State(position, consecutive, loss)
consider = [Position(0, 0)]
while consider:
    test = consider.pop(0)

pass
