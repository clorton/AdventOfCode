#! /usr/bin/env python3

from pathlib import Path

with Path("02.txt").open("r") as handle:
    lines = handle.readlines()

movement = list([l.split() for l in lines])
movement = list(map(lambda t: (t[0], int(t[1])), movement))

mapping = {
    "forward": (1, 0),
    "down": (0, 1),
    "up": (0, -1)
}

position = 0
depth = 0

for move in movement:
    position += mapping[move[0]][0] * move[1]
    depth += mapping[move[0]][1] * move[1]

print(f"Final {position=} and {depth=} ({position*depth}).")

position = 0
depth = 0
aim = 0

for move in movement:
    position += mapping[move[0]][0] * move[1]
    if move[0] == "forward":
        depth += aim * move[1]
    aim += mapping[move[0]][1] * move[1]

print(f"Final {position=} and {depth=} ({position*depth}).")

pass