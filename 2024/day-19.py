from pathlib import Path
# import re

import numpy as np
# from tqdm import tqdm

with (Path(__file__).parent / "day-19.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

width = height = 71
count = 1024

# lines = [
#     "5,4",
#     "4,2",
#     "4,5",
#     "3,0",
# ]

print("Done!")
