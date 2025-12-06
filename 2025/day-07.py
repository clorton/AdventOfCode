from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-07.txt").open("rt") as file:
    lines = [line.strip("\n") for line in file.readlines()]

print("done")
