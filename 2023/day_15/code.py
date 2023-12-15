#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

# Determine the ASCII code for the current character of the string.
# Increase the current value by the ASCII code you just determined.
# Set the current value to itself multiplied by 17.
# Set the current value to the remainder of dividing itself by 256.

input = "".join(input)

def gethash(input):
    value = 0
    for c in input:
        value += ord(c)
        value *= 17
        value %= 256
    return value

hashes = [gethash(step) for step in input.split(",")]

print(f"{sum(hashes)=}")

boxes = defaultdict(list)
for step in input.split(","):
    if step[-1] == "-":
        label = step[:-1]
        box = gethash(label)
        boxes[box] = [lens for lens in boxes[box] if lens[0] != label]
    else:
        label, focal = step.split("=")
        box = gethash(label)
        replaced = False
        for index, lens in enumerate(boxes[box]):
            if lens[0] == label:
                boxes[box][index] = (label, int(focal))
                replaced = True
                break
        if not replaced:
            boxes[box].append((label, int(focal)))

# One plus the box number of the lens in question.
# The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
# The focal length of the lens.
def power(box, slot, focal):
    return (box + 1) * (slot + 1) * focal

powers = []
for key, value in boxes.items():
    for index, lens in enumerate(value):
        powers.append(power(key, index, lens[1]))

print(f"{sum(powers)=}")

pass
