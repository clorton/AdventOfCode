#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

width = max(map(len, input))
data = np.full((len(input)+2, width+2), ord("."), dtype=np.int8)
for index, line in enumerate(input):
    data[index+1, 1:-1] = list(map(ord, line))

numbas = []
for y in range(1, data.shape[0]):
    number = 0
    adjacent = False
    for x in range(1, data.shape[1]):
        test = chr(data[y,x])
        if test in "0123456789":
            number *= 10
            number += int(test)
            if not adjacent:
                for j in [-1, 0, 1]:
                    for i in [-1, 0, 1]:
                        if chr(data[y+j,x+i]) not in ".0123456789":
                            adjacent = True
        else:
            if adjacent:
                numbas.append(number)
            number = 0
            adjacent = False
    if adjacent:
        numbas.append(number)
    number = 0
    adjacent = False

print(f"{sum(numbas)=}")

gears = defaultdict(list)
for y in range(1, data.shape[0]):
    number = 0
    gear = None
    for x in range(1, data.shape[1]):
        test = chr(data[y,x])
        if test in "0123456789":
            number *= 10
            number += int(test)
            if gear is None:
                for j in [-1, 0, 1]:
                    for i in [-1, 0, 1]:
                        if chr(data[y+j,x+i]) == "*":
                            gear = (y+j,x+i)
        else:
            if gear is not None:
                gears[gear].append(number)
            number = 0
            gear = None
    if gear is not None:
        gears[gear].append(number)
    number = 0
    adjacent = False

total = 0
for value in gears.values():
    if len(value) == 2:
        total += value[0]*value[1]

print(f"{total=}")

pass
