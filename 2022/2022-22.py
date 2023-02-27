"""Solution for Advent of Code 2022 Day 22 Challenge"""

# from collections import namedtuple
# from math import isnan, nan
# from numbers import Number
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / "2022-22.txt"

def get_inputs(filename:Path = INPUTFILE) -> List[str]:

    """Read inputs from given filename."""

    with filename.open("r") as file:
        inputs = [line.rstrip() for line in file.readlines()]

    # test = [
    # ]
    # inputs = test

    # for i in range(min(8, len(inputs))):
    #     print(f"{inputs[i]=}")

    return inputs


def main(do_part1:bool=True, do_part2:bool=True) -> None:

    """Docstring"""

    if do_part1:

        part1()

    if do_part2:

        part2()

    # return

SPACE = 0
DOT = ord(".")
WALL = ord("#")

EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3

directions = [
    np.array([0, 1], dtype=np.int32),   # facing right/east increment X
    np.array([1, 0], dtype=np.int32),   # facing down/south increment Y
    np.array([0,-1], dtype=np.int32),   # facing left/west decrement X
    np.array([-1,0], dtype=np.int32),   # facing up/north decrement Y
]


def move(position:np.ndarray, distance:int, delta:np.ndarray, tiles:np.ndarray) -> np.ndarray:

    """Docstring"""

    test = np.array(position)

    for _ in range(distance):

        test += delta       # look at next tile in given direction
        test %= len(tiles)  # wrap around as necessary

        if tiles[test[0], test[1]] == DOT:
            position[:] = test[:]   # update and keep going
            continue

        if tiles[test[0], test[1]] == WALL:
            break                   # stop here, position doesn't update any more

        assert tiles[test[0], test[1]] == SPACE, \
            f"tile[{test[0]},{test[1]}] ({tiles[test[0], test[1]]}) isn't SPACE, DOT or WALL?"

        while tiles[test[0], test[1]] == SPACE:
            test += delta
            test %= len(tiles)  # wrap around when necessary

        if tiles[test[0], test[1]] == DOT:
            position[:] = test[:]   # update and keep going
            continue

        if tiles[test[0], test[1]] == WALL:
            break                   # stop here, position doesn't update any more

    return position


def part1() -> None:

    """Docstring"""

    inputs = get_inputs()
    tiles, instructions = process_inputs(inputs)
    ix = np.nonzero(tiles[0,:] == DOT)[0][0]
    position = np.array([0,ix], dtype=np.int32)
    facing = EAST
    delta = directions[facing]
    for instruction in instructions:
        if isinstance(instruction, int):
            position = move(position, instruction, delta, tiles)
        elif instruction == "R":    # turn 90° right (east -> south -> west -> north)
            facing = (facing + 1) % len(directions)
            delta = directions[facing]
        elif instruction == "L":    # turn 90° left (east -> north -> west -> south)
            facing = (facing - 1) % len(directions)
            delta = directions[facing]
        else:
            raise RuntimeError(f"Unknown instruction ({instruction}) in instructions.")

    print(f"Part 1: final position ({position}) and facing {facing} gives password {((position+1)*np.array([1000,4], dtype=np.int32)).sum()+facing}")

    # return


def move2(position:np.ndarray, distance:int, facing:int, tiles:np.ndarray) -> Tuple[np.ndarray, int]:

    """Docstring"""

    test = np.array(position)
    delta = directions[facing]

    for _ in range(distance):

        test += delta       # look at next tile in given direction
        test %= len(tiles)  # wrap around as necessary

        if tiles[test[0], test[1]] == DOT:
            position[:] = test[:]   # update and keep going
            continue

        if tiles[test[0], test[1]] == WALL:
            break                   # stop here, position doesn't update any more

        assert tiles[test[0], test[1]] == SPACE, \
            f"tile[{test[0]},{test[1]}] ({tiles[test[0], test[1]]}) isn't SPACE, DOT or WALL?"

        yface = test[0] // 50
        xface = test[1] // 50
        why, exx = test

        if (yface,xface) == (0,0) and facing == WEST:
            # off A west -> E west
            test[:] = (149-why,0)
            facing = EAST
        elif (yface,xface) == (3,1) and facing == NORTH:
            # off A north -> F west
            test[:] = (exx+100,0)
            facing = EAST
        elif (yface,xface) == (0,3) and facing == EAST:
            # off B east -> D east
            test[:] = (149-why,99)
            facing = WEST
        elif (yface,xface) == (1,2) and facing == SOUTH:
            # off B south -> C east
            test[:] = (exx-50,99)
            facing = WEST
        elif (yface,xface) == (3,2) and facing == NORTH:
            # off B north -> F south
            test[:] = (199,exx-100)
            facing = NORTH
        elif (yface,xface) == (1,2) and facing == EAST:
            # off C east -> B south
            test[:] = (49,why+50)
            facing = NORTH
        elif (yface,xface) == (1,0) and facing == WEST:
            # off C west -> E north
            test[:] = (100,why-50)
            facing = SOUTH
        elif (yface,xface) == (2,3) and facing == WEST:
            # off E west -> A west
            test[:] = (149-why,50)
            facing = EAST
        elif (yface,xface) == (1,0) and facing == NORTH:
            # off E north -> C west
            test[:] = (50+exx,50)
            facing = EAST
        elif (yface,xface) == (2,2) and facing == EAST:
            # off D east -> B east
            test[:] = (149-why,149)
            facing = WEST
        elif (yface,xface) == (3,1) and facing == SOUTH:
            # off D south -> F east
            test[:] = (exx+100,49)
            facing = WEST
        elif (yface,xface) == (3,1) and facing == EAST:
            # off F east -> D south
            test[:] = (149,why-100)
            facing = NORTH
        elif (yface,xface) == (0,0) and facing == SOUTH:
            # off F south -> B north
            test[:] = (0,100+exx)
            facing = SOUTH
        elif (yface,xface) == (3,3) and facing == WEST:
            # off F west -> A north
            test[:] = (0,why-100)
            facing = SOUTH
        else:
            raise RuntimeError(f"Went off the edge of the world! {test=} {facing=}")

        delta = directions[facing]

        if tiles[test[0], test[1]] == DOT:
            position[:] = test[:]   # update and keep going
            continue

        if tiles[test[0], test[1]] == WALL:
            break                   # stop here, position doesn't update any more

    return position, facing

COMPASS = [ "east", "south", "west", "north" ]


def part2() -> None:

    """Docstring"""

    inputs = get_inputs()
    tiles, _ = process_inputs(inputs)
    tiles[tiles == WALL] = DOT

    # A EAST
    position, facing = move2(np.array([10,60], dtype=np.int32), 50, EAST, tiles)
    assert np.array_equal(position, np.array([10,110], dtype=np.int32))
    assert facing == EAST
    # A SOUTH
    position, facing = move2(np.array([10,60], dtype=np.int32), 50, SOUTH, tiles)
    assert np.array_equal(position, np.array([60,60], dtype=np.int32))
    assert facing == SOUTH
    # A WEST
    position, facing = move2(np.array([10,60], dtype=np.int32), 50, WEST, tiles)
    assert np.array_equal(position, np.array([139,39], dtype=np.int32))
    assert facing == EAST
    # A NORTH
    position, facing = move2(np.array([10,60], dtype=np.int32), 50, NORTH, tiles)
    assert np.array_equal(position, np.array([160,39], dtype=np.int32))
    assert facing == EAST
    # B EAST
    position, facing = move2(np.array([10,110], dtype=np.int32), 50, EAST, tiles)
    assert np.array_equal(position, np.array([139,89], dtype=np.int32))
    assert facing == WEST
    # B SOUTH
    position, facing = move2(np.array([10,110], dtype=np.int32), 50, SOUTH, tiles)
    assert np.array_equal(position, np.array([60,89], dtype=np.int32))
    assert facing == WEST
    # B WEST
    position, facing = move2(np.array([10,110], dtype=np.int32), 50, WEST, tiles)
    assert np.array_equal(position, np.array([10,60], dtype=np.int32))
    assert facing == WEST
    # B NORTH
    position, facing = move2(np.array([10,110], dtype=np.int32), 50, NORTH, tiles)
    assert np.array_equal(position, np.array([160,10], dtype=np.int32))
    assert facing == NORTH
    # C EAST
    position, facing = move2(np.array([60,60], dtype=np.int32), 50, EAST, tiles)
    assert np.array_equal(position, np.array([39,110], dtype=np.int32))
    assert facing == NORTH
    # C SOUTH
    position, facing = move2(np.array([60,60], dtype=np.int32), 50, SOUTH, tiles)
    assert np.array_equal(position, np.array([110,60], dtype=np.int32))
    assert facing == SOUTH
    # C WEST
    position, facing = move2(np.array([60,60], dtype=np.int32), 50, WEST, tiles)
    assert np.array_equal(position, np.array([139,10], dtype=np.int32))
    assert facing == SOUTH
    # C NORTH
    position, facing = move2(np.array([60,60], dtype=np.int32), 50, NORTH, tiles)
    assert np.array_equal(position, np.array([10,60], dtype=np.int32))
    assert facing == NORTH
    # D EAST
    position, facing = move2(np.array([110,60], dtype=np.int32), 50, EAST, tiles)
    assert np.array_equal(position, np.array([39,139], dtype=np.int32))
    assert facing == WEST
    # D SOUTH
    position, facing = move2(np.array([110,60], dtype=np.int32), 50, SOUTH, tiles)
    assert np.array_equal(position, np.array([160,39], dtype=np.int32))
    assert facing == WEST
    # D WEST
    position, facing = move2(np.array([110,60], dtype=np.int32), 50, WEST, tiles)
    assert np.array_equal(position, np.array([110,10], dtype=np.int32))
    assert facing == WEST
    # D NORTH
    position, facing = move2(np.array([110,60], dtype=np.int32), 50, NORTH, tiles)
    assert np.array_equal(position, np.array([60,60], dtype=np.int32))
    assert facing == NORTH
    # E EAST
    position, facing = move2(np.array([110,10], dtype=np.int32), 50, EAST, tiles)
    assert np.array_equal(position, np.array([110,60], dtype=np.int32))
    assert facing == EAST
    # E SOUTH
    position, facing = move2(np.array([110,10], dtype=np.int32), 50, SOUTH, tiles)
    assert np.array_equal(position, np.array([160,10], dtype=np.int32))
    assert facing == SOUTH
    # E WEST
    position, facing = move2(np.array([110,10], dtype=np.int32), 50, WEST, tiles)
    assert np.array_equal(position, np.array([39,89], dtype=np.int32))
    assert facing == EAST
    # E NORTH
    position, facing = move2(np.array([110,10], dtype=np.int32), 50, NORTH, tiles)
    assert np.array_equal(position, np.array([60,89], dtype=np.int32))
    assert facing == EAST
    # F EAST
    position, facing = move2(np.array([160,10], dtype=np.int32), 50, EAST, tiles)
    assert np.array_equal(position, np.array([139,60], dtype=np.int32))
    assert facing == NORTH
    # F SOUTH
    position, facing = move2(np.array([160,10], dtype=np.int32), 50, SOUTH, tiles)
    assert np.array_equal(position, np.array([10,110], dtype=np.int32))
    assert facing == SOUTH
    # F WEST
    position, facing = move2(np.array([160,10], dtype=np.int32), 50, WEST, tiles)
    assert np.array_equal(position, np.array([39,60], dtype=np.int32))
    assert facing == SOUTH
    # F NORTH
    position, facing = move2(np.array([160,10], dtype=np.int32), 50, NORTH, tiles)
    assert np.array_equal(position, np.array([110,10], dtype=np.int32))
    assert facing == NORTH

    inputs = get_inputs()
    tiles, instructions = process_inputs(inputs)
    ix = np.nonzero(tiles[0,:] == DOT)[0][0]
    position = np.array([0,ix], dtype=np.int32)
    facing = EAST
    for instruction in instructions:
        if isinstance(instruction, int):
            # print(f"Moving {instruction} tiles from {position} {COMPASS[facing]}...", end="")
            position, facing = move2(position, instruction, facing, tiles)
            # print(f"ended up at {position} facing {COMPASS[facing]}.")
        elif instruction == "R":    # turn 90° right (east -> south -> west -> north)
            facing = (facing + 1) % len(directions)
        elif instruction == "L":    # turn 90° left (east -> north -> west -> south)
            facing = (facing - 1) % len(directions)
        else:
            raise RuntimeError(f"Unknown instruction ({instruction}) in instructions.")

    # XXX Part 2: final position ([50 64]) and facing 3 gives password 51263 XXX
    print(f"Part 2: final position ({position}) and facing {facing} gives password {((position+1)*np.array([1000,4], dtype=np.int32)).sum()+facing}")

    # return


def process_inputs(inputs:List[str]) -> Tuple[np.ndarray, List[Union[int, str]]]:

    """Docstring"""

    isep = inputs.index("")
    height = isep
    width = max(map(len, inputs[:isep]))
    height = width = max(height, width) # make the tiles array square (simplifies wrapping around)
    tiles = np.zeros((height, width), dtype=np.uint8)

    for y, line in enumerate(inputs[:isep]):
        for x, tile in enumerate(line):
            if tile == ".":
                tiles[y,x] = DOT
            elif tile == "#":
                tiles[y,x] = WALL

    instructions = []
    distance = "0"
    for character in inputs[isep+1]:
        if character in "0123456789":
            distance += character
        else:
            instructions.append(int(distance))
            distance = "0"
            instructions.append(character)
    if distance != "0":
        instructions.append(int(distance))

    return tiles, instructions


if __name__ == "__main__":
    main(True, True)
