"""Solution for Advent of Code 2022 Day 20 Challenge"""

# from collections import namedtuple
from pathlib import Path
from typing import List, Union

import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / "2022-20.txt"

def get_inputs(filename:Path = INPUTFILE) -> List[Union[str,int]]:

    """Read inputs from given filename."""

    with filename.open("r") as file:
        inputs = [int(line.strip()) for line in file.readlines()]

    inputs = np.array(inputs, dtype=np.int64)
    # test = np.array([1,2,-3,3,-2,0,4], dtype=np.int64)
    # inputs = test

    print(inputs[0:8])

    return inputs


def mix(values:np.ndarray, indexes:np.ndarray) -> None:

    """Docstring"""

    for index, value in enumerate(values):

        old = indexes[index]
        new = (old + value) % (len(values)-1)
        if new == old:
            continue
        if new > old:
            indexes[(indexes > old) & (indexes <= new)] -= 1
        else:   # new < old
            indexes[(indexes >= new) & (indexes < old)] += 1
        indexes[index] = new

    # return


def coords(values:np.ndarray, indexes:np.ndarray) -> np.ndarray:

    """Docstring"""

    izero = np.nonzero(values == 0)[0][0]
    jzero = indexes[izero]
    onek = values[np.nonzero(indexes == ((jzero+1000)%len(values)))[0][0]]
    twok = values[np.nonzero(indexes == ((jzero+2000)%len(values)))[0][0]]
    thrk = values[np.nonzero(indexes == ((jzero+3000)%len(values)))[0][0]]

    return np.array([onek, twok, thrk], dtype=np.int64)


def main(part1:bool=True, part2:bool=True) -> None:

    """Docstring"""

    if part1:

        values = np.array(get_inputs(), dtype=np.int64)
        indexes = np.arange(len(values), dtype=np.int64)

        mix(values, indexes)

        coordinates = coords(values, indexes)

        print(f"Part 1: {coordinates=} => {sum(coordinates)}")
        print("Expected 4, -3, 2 => -3 for test data.")
        print("Expected 6439, 853, 7596 => 1488 for actual data.")

    if part2:

        values = np.array(get_inputs(), dtype=np.int64)*811589153
        indexes = np.arange(len(values), dtype=np.int64)

        for _ in range(10):
            mix(values, indexes)

        coordinates = coords(values, indexes)

        print(f"Part 2: {coordinates=} => {sum(coordinates)}")
        print("Expected 811589153, 2434767459, -1623178306 => 1623178306 for test data.")
        print("Expected 6187555702472, 3134357308886, -5561820465509 => 3760092545849 for actual data.")

    # return


if __name__ == "__main__":
    main(True, True)
