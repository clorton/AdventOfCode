#! /usr/bin/env python3

from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()

with (WORKING_DIRECTORY / "day-01.txt").open("r") as file:
    input = [line.strip() for line in file.readlines()]

concat = ",".join(input)
inventories = concat.split(",,")

inventories = [inventory.split(",") for inventory in inventories]
inventories = [np.array(list(map(int, inventory)), dtype=np.uint32) for inventory in inventories]

totals = np.array([inventory.sum() for inventory in inventories])
indices = np.argsort(totals)

print(f"Part 1: Maximum calories carried by elf {indices[-1]} - {totals[indices[-1]]} calories.")

print(f"Part 2: Top three carriers have {totals[indices[-1]] + totals[indices[-2]] + totals[indices[-3]]} calories.")

pass
