from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-04.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

print("done")
