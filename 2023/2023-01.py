#! /usr/bin/env python3

from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()

with (WORKING_DIRECTORY / "day-01.txt").open("r") as file:
    input = [line.strip() for line in file.readlines()]

