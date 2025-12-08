from collections import namedtuple
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

Point = namedtuple("Point", ["x", "y", "z"])

with Path(HERE / "day-09.txt").open("rt") as file:
    boxes = [Point(*list(map(int, line.split(",")))) for line in file.readlines()]

test = None

print("done")
