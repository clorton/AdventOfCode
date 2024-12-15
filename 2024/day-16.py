from pathlib import Path
# import re

import numpy as np

with (Path(__file__).parent / "day-16.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

verbose = False

# lines = [
#     "##########",
#     "#..O..O.O#",
#     "#......O.#",
#     "#.OO..O.O#",
#     "#..O@..O.#",
#     "#O#..O...#",
#     "#O..O..O.#",
#     "#.OO.O.OO#",
#     "#....O...#",
#     "##########",
# ]

print("Done.")
