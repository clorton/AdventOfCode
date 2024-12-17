from pathlib import Path
# import re

import numpy as np

with (Path(__file__).parent / "day-17.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "Register A: 729",
#     "Register B: 0",
#     "Register C: 0",
#     "",
#     "Program: 0,1,5,4,3,0",
# ]
# 4,6,3,5,6,3,5,2,1,0

print("Done")
