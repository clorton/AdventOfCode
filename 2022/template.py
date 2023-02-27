"""Solution for Advent of Code 2022 Day NN Challenge"""

# from collections import namedtuple
# from math import isnan, nan
# from numbers import Number
from pathlib import Path
from typing import List

# import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / f"{Path(__file__).stem}.txt"

def get_inputs(filename:Path = INPUTFILE) -> List[str]:

    """Read inputs from given filename."""

    with filename.open("r") as file:
        inputs = [line.strip() for line in file.readlines()]

    # test = [
    # ]
    # inputs = test

    for line, text in enumerate(inputs[0:8]):
        print(f"{line}: {text}")

    return inputs


def main(do_part1:bool=True, do_part2:bool=True) -> None:

    """Docstring"""

    if do_part1:

        part1()

    if do_part2:

        part2()

    # return


def part1() -> None:

    """Docstring"""

    # inputs = get_inputs()

    # return

def part2() -> None:

    """Docstring"""

    # inputs = get_inputs()

    # return


if __name__ == "__main__":
    main(True, True)
