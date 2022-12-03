#! /usr/bin/env python3

from pathlib import Path

import numpy as np

INPUT_FILE = Path(__file__.replace("py", "txt"))

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

mapping = { k:i+1 for i, k in enumerate("abcdefghijklmnopqrstuvwxyz") }
mapping.update({ k:i+27 for i, k in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ") })

total = 0
for inventory in input:
    compartment1 = inventory[:len(inventory)//2]
    compartment2 = inventory[len(inventory)//2:]
    shared = set(compartment1) & set(compartment2)
    for element in shared:
        total += mapping[element]

print(f"Part 1: total is {total}")

total = 0
for i in range(0, len(input), 3):
    badge = set(input[i]) & set(input[i+1]) & set(input[i+2])
    for element in badge:
        total += mapping[element]

print(f"Part 2: total is {total}")
