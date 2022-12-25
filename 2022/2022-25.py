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
    #     "1=-0-2",
    #     "12111",
    #     "2=0=",
    #     "21",
    #     "2=01",
    #     "111",
    #     "20012",
    #     "112",
    #     "1=-1=",
    #     "1-12",
    #     "12",
    #     "1=",
    #     "122",
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


mapping = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

reverse = {v:k for k,v in mapping.items()}

def snafu(number:int) -> str:

    """Docstring"""

    remainder = number
    accumulate = []
    while remainder > 0:
        digit = remainder % 5
        remainder //= 5
        accumulate.append(digit)

    carry = 0
    shifted = []
    for value in accumulate:
        value += carry
        if value > 2:
            value = value - 5
            carry = 1
        else:
            carry = 0
        shifted.append(value)

    translation = "".join(map(lambda d:reverse[d], reversed(shifted)))

    return translation


def part1() -> None:

    """Docstring"""

    inputs = get_inputs()

    # Sum up SNAFU coded fuel requirements

    total = 0
    for line in inputs:
        number = 0
        for place, digit in enumerate(reversed(line)):
            digit = mapping[digit]
            number += digit * pow(5,place)
        print(f"Translated '{line}' to {number}.")
        total += number

    print(f"Part 1: total (decimal) = {total}")

    # Present sum in a SNAFU coded number
    print(f"Part 1: snafu({total}) = {snafu(total)}")

    # return

def part2() -> None:

    """Docstring"""

    # inputs = get_inputs()

    # return


if __name__ == "__main__":
    main(True, False)
