#! /usr/bin/env python3

from pathlib import Path

import numpy as np

INPUT_FILE = Path(__file__.replace("py", "txt"))

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

# input = [ "A Y", "B X", "C Z"]

mapping = {
    "A": 1, # rock
    "B": 2, # paper
    "C": 3, # scissors
    "X": 1, # rock
    "Y": 2, # paper
    "Z": 3  # scissors
}

outcomes = {
    1: { 1: 3, 2: 0, 3: 6 },
    2: { 1: 6, 2: 3, 3: 0 },
    3: { 1: 0, 2: 6, 3: 3 },
}

total = 0
for round in input:
    elf, self = round.split(" ")
    elf, self = mapping[elf], mapping[self]
    total += self
    total += outcomes[self][elf]

print(f"1: Total score is {total} points.")

strategy = {
    1: { 1: 3, 2: 1, 3: 2 },    # lose
    2: { 1: 1, 2: 2, 3: 3 },    # draw
    3: { 1: 2, 2: 3, 3: 1 }     # win
}

throw_map = { 1: "rock", 2: "paper", 3: "scissors" }
strat_map = { 1: "lose", 2: "draw",  3: "win" }

total = 0
for round in input:
    elf, self = round.split(" ")
    elf, self = mapping[elf], mapping[self]
    # print(f"Elf throwing {throw_map[elf]}, strategy is {strat_map[self]}...", end="")
    self = strategy[self][elf]
    # print(f"self throwing {throw_map[self]}.")
    total += self
    total += outcomes[self][elf]

print(f"2: Total score is {total} points.")
