from pathlib import Path

import numpy as np

with (Path(__file__).parent / "day-11.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "89010123",
#     "78121874",
#     "87430965",
#     "96549874",
#     "45678903",
#     "32019012",
#     "01329801",
#     "10456732",
# ]

print("Done.")
