#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "example.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

instructions = [line.split(" ") for line in input]
instructions = [(instruction[0], int(instruction[1]), instruction[2]) for instruction in instructions]

delta = {
    "D": np.array((1, 0)),
    "U": np.array((-1, 0)),
    "R": np.array((0, 1)),
    "L": np.array((0, -1)),
    1: np.array((1, 0)),
    3: np.array((-1, 0)),
    0: np.array((0, 1)),
    2: np.array((0, -1)),
}

minx, miny = 0, 0
maxx, maxy = 0, 0
position = np.array((0, 0)) # y,x
for direction, count, color in instructions:
    for _ in range(count):
        position += delta[direction]
    minx = min(minx, position[1])
    miny = min(miny, position[0])
    maxx = max(maxx, position[1])
    maxy = max(maxy, position[0])

print(f"minx: {minx}, miny: {miny}, maxx: {maxx}, maxy: {maxy}")
width = maxx - minx + 1
height = maxy - miny + 1
print(f"width: {width}, height: {height}")
startx = -minx
starty = -miny
print(f"startx: {startx}, starty: {starty}")

dirt = np.full((height, width), ".")
position = np.array((starty, startx))
dirt[tuple(position)] = "#"
for direction, count, color in instructions:
    for _ in range(count):
        position += delta[direction]
        dirt[tuple(position)] = "#"

# for row in dirt:
#     print("".join(row))
# print("\n----------\n")

inside = False
for y in range(height-1):
    for x in range(width):
        if (dirt[y, x] == "#") and (dirt[y+1, x] == "#"):
            inside = not inside
        elif (dirt[y, x] == ".") and inside:
            dirt[y, x] = "X"

# for row in dirt:
#     print("".join(row))
# print()

print(f"{(dirt != '.').sum()=}")

# Part 2

instructions = [color[2:-1] for direction, count, color in instructions]
instructions = [[int(instruction[0:-1],16), int(instruction[-1])] for instruction in instructions]

minx, miny = 0, 0
maxx, maxy = 0, 0
position = np.array((0, 0)) # y,x
for count, direction in instructions:
    position += delta[direction] * count
    minx = min(minx, position[1])
    miny = min(miny, position[0])
    maxx = max(maxx, position[1])
    maxy = max(maxy, position[0])

print(f"minx: {minx}, miny: {miny}, maxx: {maxx}, maxy: {maxy}")
width = maxx - minx + 1
height = maxy - miny + 1
print(f"width: {width}, height: {height}")
startx = -minx
starty = -miny
print(f"startx: {startx}, starty: {starty}")

pass
