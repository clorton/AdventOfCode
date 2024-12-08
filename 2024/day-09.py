from pathlib import Path

# import numpy as np

with (Path(__file__).parent / "day-08.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "............",
#     "........0...",
#     ".....0......",
#     ".......0....",
#     "....0.......",
#     "......A.....",
#     "............",
#     "............",
#     "........A...",
#     ".........A..",
#     "............",
#     "............",
# ]

print("Done.")
