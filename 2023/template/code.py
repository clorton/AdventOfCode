#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

pass
