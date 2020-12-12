#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-12.txt").read_text()

# text = "F10\nN3\nF7\nR90\nF11"    # Part 1 = 25, Part 2 = 286

lines = text.split("\n")
actions = [(line[0], int(line[1:])) for line in lines]


# part 1
EAST = 0
SOUTH = 90
WEST = 180
NORTH = 270
deltas = {
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
    "N": (0, 1)
}
directions = {
    0: "E",
    270: "S",
    180: "W",
    90: "N"
}
facing = EAST
x = 0
y = 0
for instruction, distance in actions:
    if instruction in ["E", "S", "W", "N"]:
        dx, dy = deltas[instruction]
        x += dx * distance
        y += dy * distance
    elif instruction == "R":
        facing -= distance
        facing %= 360
    elif instruction == "L":
        facing += distance
        facing %= 360
    elif instruction == "F":
        dx, dy = deltas[directions[facing]]
        x += dx * distance
        y += dy * distance

print(f"Part 1: Final location ({x}, {y}), Manhattan distance = {abs(x)+abs(y)}.")


# part 2
facing = EAST
wx = 10
wy = 1
sx = 0
sy = 0
for instruction, distance in actions:
    if instruction in ["E", "S", "W", "N"]:
        dx, dy = deltas[instruction]
        wx += dx * distance
        wy += dy * distance
    elif instruction == "R":
        for _ in range(distance // 90):
            wx, wy = wy, -wx
            distance -= 90
    elif instruction == "L":
        for _ in range(distance // 90):
            wx, wy = -wy, wx
            distance -= 90
    elif instruction == "F":
        sx += wx * distance
        sy += wy * distance

print(f"Part 2: Final location ({sx}, {sy}), Manhattan distance = {abs(sx)+abs(sy)}.")


print(".oO( done )")
