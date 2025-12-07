from collections import namedtuple
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-08.txt").open("rt") as file:
    lines = [list(map(ord, line.strip("\n"))) for line in file.readlines()]

print("done")
