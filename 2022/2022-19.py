"""Solution for Advent of Code 2022 Day NN Challenge"""

from collections import defaultdict
# from collections import namedtuple
# from functools import lru_cache
# from math import isnan, nan
# from numbers import Number
from pathlib import Path
from typing import List

import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / f"{Path(__file__).stem}.txt"

def get_inputs(filename:Path = INPUTFILE, example:bool = False) -> List[str]:

    """Read inputs from given filename."""

    with filename.open("r") as file:
        inputs = [line.strip() for line in file.readlines()]

    if example:
        test = [
            "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.",
            "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."
        ]
        inputs = test

    for line, text in enumerate(inputs[0:16]):
        print(f"{line}: {text}")

    return inputs


def main(do_part1:bool=True, do_part2:bool=True) -> None:

    """Docstring"""

    if do_part1:

        part1()

    if do_part2:

        part2()

    # return

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
COUNT = 4


def get_blueprints(inputs:List[str]) -> np.ndarray:

    """Docstring"""

    blueprints = np.zeros((len(inputs), COUNT, COUNT), dtype=np.uint8)
    for line in inputs:
        line = line.split(" ")
        blueprint_id = int(line[1][:-1])
        ore_ore_cost = int(line[6])
        clay_ore_cost = int(line[12])
        obisidian_ore_cost = int(line[18])
        obisidian_clay_cost = int(line[21])
        geode_ore_cost = int(line[27])
        geode_obsidian_cost = int(line[30])
        index = blueprint_id -1
        blueprints[index,ORE,ORE] = ore_ore_cost
        blueprints[index,CLAY,ORE] = clay_ore_cost
        blueprints[index,OBSIDIAN,ORE] = obisidian_ore_cost
        blueprints[index,OBSIDIAN,CLAY] = obisidian_clay_cost
        blueprints[index,GEODE,ORE] = geode_ore_cost
        blueprints[index,GEODE,OBSIDIAN] = geode_obsidian_cost

    return blueprints


def max_geodes(blueprint:np.ndarray, clock:int=0, robots:np.ndarray=np.array([1,0,0,0],dtype=np.int8), resources:np.ndarray=np.zeros(4, dtype=np.int8)) -> int:

    """Docstring"""

    if clock % 5 == 0:
        print(f"{clock:2}: {robots=}, {resources=}")

    if clock >= 24:
        return resources[GEODE]

    maximum = 0

    for robot, cost in enumerate(reversed(blueprint)):
        if np.all(resources >= cost):
            # print(f"Building robot {robot} at time {clock} ({resources=}, {cost=})")
            resources -= cost
            resources += robots
            robots[robot] += 1
            geodes = max_geodes(blueprint, clock+1, robots, resources)
            robots[robot] -= 1
            resources -= robots
            resources += cost

            maximum = max(maximum, geodes)

    # If we build nothing (action = None), just collect:
    resources += robots
    maximum = max(maximum, max_geodes(blueprint, clock+1, robots, resources))
    resources -= robots


    return maximum


def explore(blueprint:np.ndarray, clock:int=0, robots:np.ndarray=np.array([1,0,0,0],dtype=np.int8), resources:np.ndarray=np.zeros(4, dtype=np.int8), debug:bool=False) -> int:

    states = defaultdict(set)
    states[0].add((robots.tobytes(), resources.tobytes()))
    while True:

        clock = max(states.keys())
        print(f"{clock:2}: {len(states[clock])}, ", end="")

        tick = clock + 1

        obsidian = False
        geodes = 0

        for robots, resources in states[clock]:

            robots = np.array(np.frombuffer(robots, dtype=np.uint8))
            resources = np.array(np.frombuffer(resources, dtype=np.uint8))

            states[tick].add( (robots.tobytes(), (resources+robots).tobytes()) )

            for robot, cost in enumerate(blueprint):
                if np.all(resources >= cost):
                    resources -= cost
                    resources += robots
                    robots[robot] += 1
                    obsidian |= resources[OBSIDIAN] > 0
                    geodes   = max(geodes,resources[GEODE])
                    states[tick].add( (robots.tobytes(), resources.tobytes()) )
                    robots[robot] -= 1
                    resources -= robots
                    resources += cost

        if geodes > 0:
            states[tick] = {(robots, resources) for robots, resources in states[tick] if np.frombuffer(resources, dtype=np.uint8)[GEODE] == geodes}
        elif obsidian:
            states[tick] = {(robots, resources) for robots, resources in states[tick] if np.frombuffer(resources, dtype=np.uint8)[OBSIDIAN] > 0}

        if tick == 24:
            break

    print()

    return states[24]


def part1() -> None:

    """Docstring"""

    use_example = True

    inputs = get_inputs(example=use_example)
    blueprints = get_blueprints(inputs)

    if use_example:
#        print(f"{max_geodes(blueprints[0], clock=0)=}")
#        print(f"{max_geodes(blueprints[-1])=}")
        temp1 = explore(blueprints[0], debug=True)
        max1 = max(map(lambda e: np.frombuffer(e[1], dtype=np.uint8)[GEODE], temp1))
        print(f"{max1=}")
        temp2 = explore(blueprints[-1], debug=True)
        max2 = max(map(lambda e: np.frombuffer(e[1], dtype=np.uint8)[GEODE], temp2))
        print(f"{max2=}")
    else:
        total = 0
        for index, blueprint in enumerate(blueprints):
            print(inputs[index])
            print(f"{index:2}: ", end="")
            states = explore(blueprint)
            maximum = max(map(lambda e: np.frombuffer(e[1], dtype=np.uint8)[GEODE], states))
            print(f"{maximum=}")
            total += maximum
        print(f"Part 1: {total=}")

    return

def part2() -> None:

    """Docstring"""

    # inputs = get_inputs()

    # return


if __name__ == "__main__":
    main(True, True)
