from pathlib import Path
import re

import numpy as np

with (Path(__file__).parent / "day-06.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

print("Done.")
