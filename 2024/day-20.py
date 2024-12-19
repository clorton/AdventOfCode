from pathlib import Path
# import re

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "day-20.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "r, wr, b, g, bwu, rb, gb, br",
#     "",
#     "brwrr",
#     "bggr",
#     "gbbr",
#     "rrbgbr",
#     "ubwu",
#     "bwurrg",
#     "brgr",
#     "bbrgwb",
# ]

print("Done!")
