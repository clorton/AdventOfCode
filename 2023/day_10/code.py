#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from functools import reduce
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

height = len(input)
width = len(input[0])

VERT = ord("|")
HORZ = ord("-")
NE = ord("L")
SE = ord("F")
SW = ord("7")
NW = ord("J")
DOT = ord(".")
ANIMAL = ord("S")
STAR = ord("*")

pipes = np.full((height+2, width+2), fill_value=DOT, dtype=np.uint8)

for i, line in enumerate(input):
    pipes[i+1,1:-1] = list(map(ord, line))

find = list(filter(lambda e: "S" in e[1], enumerate(input)))
ay = find[0][0] + 1
ax = find[0][1].index("S") + 1

Delta = namedtuple("Delta", ["dx", "dy"])
# north, east, south, west
directions = [Delta(0,-1), Delta(1,0), Delta(0,1), Delta(-1,0)]

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

moves = {
    ANIMAL: [NORTH,EAST,SOUTH,WEST],
    VERT: [NORTH,SOUTH],
    NE: [NORTH,EAST],
    HORZ: [EAST,WEST],
    SE: [EAST, SOUTH],
    SW: [SOUTH, WEST],
    NW: [NORTH, WEST],
}

valid = {
    directions[NORTH]: [SE, SW, VERT],
    directions[EAST]: [NW, SW, HORZ],
    directions[SOUTH]: [NW, NE, VERT],
    directions[WEST]: [NE, SE, HORZ]
}

Position = namedtuple("Position", ["x", "y", "d"])
identified = []
totest = [Position(ax, ay, 0)]
mutable = np.array(pipes, dtype=np.uint8)
while totest:

    position = totest.pop(0)

    px, py, d = position
    kind = mutable[py,px]
    if kind == STAR:
        continue
    mutable[py,px] = STAR

    for direction in moves[kind]:
        direction = directions[direction]
        testx = px + direction.dx
        testy = py + direction.dy
        test = mutable[testy, testx]
        if test in valid[direction]:
            totest.append(Position(testx, testy, d+1))
    
    identified.append(position)

captcha = list(reduce(lambda a, b : a if a.d >= b.d else b, identified))
print(f"{captcha=}")

# scans = defaultdict(list)
# for tile in identified:
#     scans[tile.y].append(tile)
# scans = {y:list(sorted(v)) for y,v in scans.items()}

# contained = 0
# inside = False
# for scan in scans.values():
#     x = 1
#     for pipe in scan:
#         run = pipe.x - x
#         if inside:
#             contained += run
#         x = pipe.x + 1
#         inside = not inside

# print(f"{contained=}")

contained = 0
for y in range(1,mutable.shape[0]-1):
    print(f"{''.join(map(chr,mutable[y]))}", end="")
    inside = False
    bars = 0
    for x in range(1, mutable.shape[1]-1):
        if mutable[y,x] != STAR:
            if inside:
                contained += 1
        else:
            tile = pipes[y,x]
            inside, bars = {
                VERT: lambda i,_b : (not i,0),
                HORZ: lambda i,b : (i,b),
                NE: lambda i,_b : (i,1),
                SE: lambda i,_b : (i,-1),
                SW: lambda i,b : [(i,0),(None),(not i,0)][b+1],
                ANIMAL: lambda i,b : [(i,0),(None),(not i,0)][b+1],
                NW: lambda i,b : [(not i,0),(None),(i,0)][b+1],
            }[tile](inside, bars)
    print(f"{contained=}")

print(f"{contained=}")

pass
