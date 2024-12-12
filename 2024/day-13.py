from pathlib import Path

import numpy as np

with (Path(__file__).parent / "day-13.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

lines = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE",
]

print("Done.")
