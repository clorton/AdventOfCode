"""Solution for Advent of Code 2022 Day 24 Challenge"""

from collections import namedtuple
from functools import lru_cache
# from math import isnan, nan
# from numbers import Number
from pathlib import Path
from typing import List

import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / f"{Path(__file__).stem}.txt"

def get_inputs(filename:Path = INPUTFILE) -> List[str]:

    """Read inputs from given filename."""

    print(f"Getting inputs from '{filename}'...")
    with filename.open("r") as file:
        inputs = [line.strip() for line in file.readlines()]

    # test = [
    #     "#.######",
    #     "#>>.<^<#",
    #     "#.<..<<#",
    #     "#>v.><>#",
    #     "#<^v^^>#",
    #     "######.#",
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


MAPPING = {
    0x00: "•",
    0x01: "^",
    0x02: ">",
    0x03: "2",
    0x04: "v",
    0x05: "2",
    0x06: "2",
    0x07: "3",
    0x08: "<",
    0x09: "2",
    0x0A: "2",
    0x0B: "3",
    0x0C: "2",
    0x0D: "3",
    0x0E: "3",
    0x0F: "4",
    0xF0: "#",
}


def display_valley(valley:np.ndarray) -> None:

    """Docstring"""

    for row in valley:
        print("".join(list(map(lambda b:MAPPING[b],row))))

    print()

    # return

Delta = namedtuple("Delta", ["dy", "dx"])
MOVEMENT = [
    Delta(-1,0),    # "^"
    Delta(0,1),     # ">"
    Delta(1,0),     # "v"
    Delta(0,-1),    # "<"
]

@lru_cache
def wrapping(size:int) -> np.ndarray:

    wrap = np.arange(size)
    wrap[1],wrap[-2] = wrap[-2]-1,wrap[1]+1

    return wrap



def update_weather(inow:int,inext:int,valley:np.ndarray) -> None:

    """Docstring"""

    wrapy = wrapping(valley.shape[1])
    wrapx = wrapping(valley.shape[2])

    today = valley[inow,:,:]
    tomorrow = valley[inext,:,:]

    tomorrow[1,2]       = 0     # entrance
    tomorrow[2:-2,2:-2] = 0     # valley floor
    tomorrow[-2,-3]     = 0     # exit

    for y in range(2,valley.shape[1]-2):
        for x in range(2,valley.shape[2]-2):
            cell = today[y,x]
            for direction in range(4):
                if cell & (blizzard := 1<<direction):
                    yprime = wrapy[y + MOVEMENT[direction].dy]
                    xprime = wrapx[x + MOVEMENT[direction].dx]
                    tomorrow[yprime,xprime] |= blizzard

    # return

CONSIDER = [
    # dy,dx order
    [0,0],  # wait
    [0,1],  # east
    [1,0],  # south
    [0,-1], # west
    [-1,0]  # north
]


def part1() -> None:

    """Docstring"""

    inputs = get_inputs()

    valley = np.full((2, len(inputs)+2, max(map(len,inputs))+2),0xF0, dtype=np.uint8)
    for y, line in enumerate(inputs):
        valley[0,y+1,1:-1] = list(map(ord,line))

    valley[valley == ord(".")] = 0x00
    valley[valley == ord("^")] = 0x01
    valley[valley == ord(">")] = 0x02
    valley[valley == ord("v")] = 0x04
    valley[valley == ord("<")] = 0x08
    valley[valley == ord("#")] = 0xF0

    yfinish,xfinish = len(inputs),max(map(len,inputs))-1

    possibilities = np.zeros_like(valley, dtype=np.uint8)
    possibilities[0,1,2] = 1

    minute = 0
    while possibilities[minute%2,yfinish,xfinish] == 0:

        if minute%10 == 0: print(".", end="")

        inow = minute % 2
        inext = (minute+1)%2

        update_weather(inow,inext,valley)

        updated = valley[inext,:,:]

        prospects = possibilities[inext,:,:]
        prospects[:,:] = 0

        for ye,xe in zip(*np.nonzero(possibilities[inow,:,:])):

            for option in CONSIDER:
                dy,dx = option
                if updated[ye+dy,xe+dx] == 0:
                    prospects[ye+dy,xe+dx] = 1

        minute += 1

    print(f"Part 1: reached the finish on minute {minute}")

    return

def part2() -> None:

    """Docstring"""

    inputs = get_inputs()

    valley = np.full((2, len(inputs)+2, max(map(len,inputs))+2),0xF0, dtype=np.uint8)
    for y, line in enumerate(inputs):
        valley[0,y+1,1:-1] = list(map(ord,line))

    valley[valley == ord(".")] = 0x00
    valley[valley == ord("^")] = 0x01
    valley[valley == ord(">")] = 0x02
    valley[valley == ord("v")] = 0x04
    valley[valley == ord("<")] = 0x08
    valley[valley == ord("#")] = 0xF0

    ystart,xstart = 1,2
    yfinish,xfinish = len(inputs),max(map(len,inputs))-1

    possibilities = np.zeros_like(valley, dtype=np.uint8)
    possibilities[0,ystart,xstart] = 1

    minute = 0
    while possibilities[minute%2,yfinish,xfinish] == 0:

        if minute%10 == 0: print(".", end="")

        inow = minute % 2
        inext = (minute+1)%2

        update_weather(inow,inext,valley)

        tomorrow = valley[inext,:,:]

        prospects = possibilities[inext,:,:]
        prospects[:,:] = 0

        for ye,xe in zip(*np.nonzero(possibilities[inow,:,:])):

            for option in CONSIDER:
                dy,dx = option
                if tomorrow[ye+dy,xe+dx] == 0:
                    prospects[ye+dy,xe+dx] = 1

        minute += 1

    print(f"\nPart 2: first traversal on minute {minute}")

    possibilities = np.zeros_like(valley, dtype=np.uint8)
    possibilities[minute%2,yfinish,xfinish] = 1

    while possibilities[minute%2,ystart,xstart] == 0:

        if minute%10 == 0: print(".", end="")

        inow = minute % 2
        inext = (minute+1)%2

        update_weather(inow,inext,valley)

        updated = valley[inext,:,:]

        prospects = possibilities[inext,:,:]
        prospects[:,:] = 0

        for ye,xe in zip(*np.nonzero(possibilities[inow,:,:])):

            for option in CONSIDER:
                dy,dx = option
                if updated[ye+dy,xe+dx] == 0:
                    prospects[ye+dy,xe+dx] = 1

        minute += 1

    print(f"\nPart 2: second traversal on minute {minute}")

    possibilities = np.zeros_like(valley, dtype=np.uint8)
    possibilities[minute%2,ystart,xstart] = 1

    while possibilities[minute%2,yfinish,xfinish] == 0:

        if minute%10 == 0: print(".", end="")

        inow = minute % 2
        inext = (minute+1)%2

        update_weather(inow,inext,valley)

        updated = valley[inext,:,:]

        prospects = possibilities[inext,:,:]
        prospects[:,:] = 0

        for ye,xe in zip(*np.nonzero(possibilities[inow,:,:])):

            for option in CONSIDER:
                dy,dx = option
                if updated[ye+dy,xe+dx] == 0:
                    prospects[ye+dy,xe+dx] = 1

        minute += 1

    print(f"\nPart 2: second traversal on minute {minute}")

    # return


if __name__ == "__main__":
    main(True, True)
