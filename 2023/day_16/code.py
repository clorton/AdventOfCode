#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

cavern = np.array([list(line) for line in input])

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

def process(cavern, start):

    visited = {
        UP: np.zeros_like(cavern, dtype=bool),
        DOWN: np.zeros_like(cavern, dtype=bool),
        LEFT: np.zeros_like(cavern, dtype=bool),
        RIGHT: np.zeros_like(cavern, dtype=bool),
    }
    # energized = np.zeros_like(cavern, dtype=np.int32)

    # state = (0,0,(1,0))
    # beams = [state]
    beams = [start]
    while beams:
        state = beams.pop(0)
        x, y, (dx, dy) = state
        while 0 <= x < cavern.shape[1] and 0 <= y < cavern.shape[0]:
            if visited[(dx,dy)][y,x]:
                break
            visited[(dx,dy)][y,x] = True
            # energized[y,x] += 1
            if cavern[y,x] == ".":
                pass
            elif cavern[y,x] == "/":
                dx, dy = -dy, -dx    
            elif cavern[y,x] == "\\":
                dx, dy = dy, dx
            elif cavern[y,x] == "|":
                if dx != 0:
                    dx, dy = 0, -1
                    beams.append((x,y+1,(0,1)))
            elif cavern[y,x] == "-":
                if dy != 0:
                    dx, dy = -1, 0
                    beams.append((x+1,y,(1,0)))
            else:
                raise ValueError(f"Unknown cavern tile: {cavern[y,x]=}")
            x += dx
            y += dy
    return visited

visited = process(cavern, (0,0,(1,0)))
energized = visited[UP] | visited[DOWN] | visited[LEFT] | visited[RIGHT]
print(f"Part 1: {(energized!=0).sum()=}")

best = 0
for x in tqdm(range(cavern.shape[1])):
    visited = process(cavern, (x,0,(0,1)))
    energized = (visited[UP] | visited[DOWN] | visited[LEFT] | visited[RIGHT]).sum()
    best = max(best, energized)
    visited = process(cavern, (x,cavern.shape[0]-1,(0,-1)))
    energized = (visited[UP] | visited[DOWN] | visited[LEFT] | visited[RIGHT]).sum()
    best = max(best, energized)

for y in tqdm(range(cavern.shape[0])):
    visited = process(cavern, (0,y,(1,0)))
    energized = (visited[UP] | visited[DOWN] | visited[LEFT] | visited[RIGHT]).sum()
    best = max(best, energized)
    visited = process(cavern, (cavern.shape[1]-1,y,(-1,0)))
    energized = (visited[UP] | visited[DOWN] | visited[LEFT] | visited[RIGHT]).sum()
    best = max(best, energized)

print(f"Part 2: {best=}")

pass
