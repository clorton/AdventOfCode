
"""Solution for Advent of Code 2022 Day 22 Challenge"""

# from collections import namedtuple
from collections import defaultdict
# from math import isnan, nan
# from numbers import Number
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / "2022-23.txt"

def get_inputs(filename:Path = INPUTFILE) -> List[str]:

    """Read inputs from given filename."""

    with filename.open("r") as file:
        inputs = [line.rstrip() for line in file.readlines()]

    # test = [
    #     ".....",
    #     "..##.",
    #     "..#..",
    #     ".....",
    #     "..##.",
    #     ".....",
    # ]
    # test = [
    #     "..............",
    #     "..............",
    #     ".......#......",
    #     ".....###.#....",
    #     "...#...#.#....",
    #     "....#...##....",
    #     "...#.###......",
    #     "...##.#.##....",
    #     "....#..#......",
    #     "..............",
    #     "..............",
    #     "..............",
    # ]
    # inputs = test

    for i in range(min(8, len(inputs))):
        print(f"{inputs[i]=}")

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

    inputs = get_inputs()

    ROUNDS = 10
    MARGIN = ROUNDS + 1

    grid = np.zeros((len(inputs)+(2*MARGIN), max(map(len, inputs))+(2*MARGIN)), dtype=np.uint8)
    for y, data in enumerate(inputs):
        grid[y+MARGIN,MARGIN:MARGIN+len(data)] = list(map(ord,data))

    grid[grid==46] = 0

    # print_grid(grid)

    ELF = ord("#")

    NEIGHBORS = np.full((3,3), ELF, dtype=np.uint8)
    NEIGHBORS[1,1] = 0

    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3

    masks = [
        np.array([1,1,1,0,0,0,0,0,0], dtype=np.uint8).reshape((3,3)),
        np.array([0,0,0,0,0,0,1,1,1], dtype=np.uint8).reshape((3,3)),
        np.array([1,0,0,1,0,0,1,0,0], dtype=np.uint8).reshape((3,3)),
        np.array([0,0,1,0,0,1,0,0,1], dtype=np.uint8).reshape((3,3)),
    ]

    steps = [ (-1,0), (1,0), (0,-1), (0,1) ]    # dy,dx

    first_consider = NORTH
    for _ in range(ROUNDS):
        # print_grid(grid)
        elves = list(zip(*np.nonzero(grid==ELF)))
        proposed = defaultdict(list)
        for elf in elves:
            y, x = elf
            if (grid[y-1:y+2,x-1:x+2] & NEIGHBORS).any():
                # at least one neighboring elf
                for consider in range(first_consider,first_consider+len(masks)):
                    consider %= len(masks)
                    if not (grid[y-1:y+2,x-1:x+2] & masks[consider]).any():
                        deltay, deltax = steps[consider]
                        destination = (y+deltay, x+deltax)
                        proposed[destination].append(elf)
                        break
        pass
        for destination, elves in proposed.items():
            if len(elves) == 1:
                y, x = elves[0]
                grid[y,x] = 0
                desty, destx = destination
                grid[desty,destx] = ELF
        first_consider = (first_consider + 1) % len(masks)

    # print_grid(grid)

    elves = np.nonzero(grid==ELF)
    minx = min(elves[1])
    maxx = max(elves[1])
    miny = min(elves[0])
    maxy = max(elves[0])

    space = np.sum(grid[miny:maxy+1,minx:maxx+1] == 0)

    print(f"Part 1: empty ground is {space} spaces")

    return


def print_grid(grid:np.ndarray) -> None:

    """Docstring"""

    elves = np.nonzero(grid==ord("#"))
    minx = min(elves[1])
    maxx = max(elves[1])
    miny = min(elves[0])
    maxy = max(elves[0])

    content = np.array(grid[miny-5:maxy+1+5,minx-5:maxx+1+5])
    content[content==0] = ord(".")

    for row in content:
        print("".join(list(map(chr,row))))

    print()

    # return



def part2() -> None:

    """Docstring"""

    inputs = get_inputs()

    MARGIN = 10_000

    grid = np.zeros((len(inputs)+(2*MARGIN), max(map(len, inputs))+(2*MARGIN)), dtype=np.uint8)
    for y, data in enumerate(inputs):
        grid[y+MARGIN,MARGIN:MARGIN+len(data)] = list(map(ord,data))

    grid[grid==46] = 0

    ELF = ord("#")

    NEIGHBORS = np.full((3,3), ELF, dtype=np.uint8)
    NEIGHBORS[1,1] = 0

    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3

    masks = [
        np.array([1,1,1,0,0,0,0,0,0], dtype=np.uint8).reshape((3,3)),
        np.array([0,0,0,0,0,0,1,1,1], dtype=np.uint8).reshape((3,3)),
        np.array([1,0,0,1,0,0,1,0,0], dtype=np.uint8).reshape((3,3)),
        np.array([0,0,1,0,0,1,0,0,1], dtype=np.uint8).reshape((3,3)),
    ]

    steps = [ (-1,0), (1,0), (0,-1), (0,1) ]    # dy,dx

    first_consider = NORTH
    round = 1
    while True:
        print(f"Round {round}...", end="")
        elves = list(zip(*np.nonzero(grid==ELF)))
        proposed = defaultdict(list)
        for elf in elves:
            y, x = elf
            if (grid[y-1:y+2,x-1:x+2] & NEIGHBORS).any():
                for consider in range(first_consider,first_consider+len(masks)):
                    consider %= len(masks)
                    if not (grid[y-1:y+2,x-1:x+2] & masks[consider]).any():
                        deltay, deltax = steps[consider]
                        destination = (y+deltay, x+deltax)
                        proposed[destination].append(elf)
                        break

        count = 0
        for destination, elves in proposed.items():
            if len(elves) == 1:
                y, x = elves[0]
                grid[y,x] = 0
                desty, destx = destination
                grid[desty,destx] = ELF
                count += 1
        print(f"moved {count} elves.")

        if count == 0:
            break

        first_consider = (first_consider + 1) % len(masks)
        round += 1

    print(f"Part 2: no elves move on round {round}")

    return


if __name__ == "__main__":
    main(False, True)
