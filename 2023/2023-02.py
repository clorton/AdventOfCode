#! /usr/bin/env python3

from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

games = [line.split(": ") for line in input]

limits = {
    "red": 12,
    "green": 13,
    "blue": 14
}

total = 0
for game in games:
    valid = True
    [name, draws] = game
    for draw in draws.split("; "):
        cubes = draw.split(", ")
        cubes = list(map(lambda x:x.split(" "), cubes))
        cubes = { e[1]: int(e[0]) for e in cubes}
        for key in cubes.keys():
            if cubes[key] > limits[key]:
                valid = False
    if valid:
        total += int(name.split(" ")[1])

print(f"{total=}")

total = 0
for game in games:
    [name, draws] = game
    minima = { "red": 0, "green": 0, "blue": 0 }
    for draw in draws.split("; "):
        cubes = draw.split(", ")
        cubes = list(map(lambda x:x.split(" "), cubes))
        cubes = { e[1]: int(e[0]) for e in cubes}
        for key in cubes.keys():
            minima[key] = max(minima[key], cubes[key])
    power = 1
    for key in minima:
        power *= minima[key]
    total += power

print(f"{total=}")

pass
