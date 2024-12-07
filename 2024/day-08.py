from pathlib import Path

# import numpy as np

with (Path(__file__).parent / "day-08.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

print("Done.")
