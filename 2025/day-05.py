from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-05.txt").open("rt") as file:
    lines = [list(map(ord, line.strip())) for line in file.readlines()]

print("done")
