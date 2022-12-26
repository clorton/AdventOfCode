"""Solution for Advent of Code 2022 Day 16 Challenge"""

from collections import defaultdict, namedtuple
from datetime import datetime
from itertools import combinations
# from math import isnan, nan
# from numbers import Number
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / f"{Path(__file__).stem}.txt"

def get_inputs(filename:Path=INPUTFILE, example:bool=False) -> List[str]:

    """Read inputs from given filename."""

    with filename.open("r") as file:
        inputs = [line.strip() for line in file.readlines()]

    if example:
        test = [
            "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
            "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
            "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
            "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
            "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
            "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
            "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
            "Valve HH has flow rate=22; tunnel leads to valve GG",
            "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
            "Valve JJ has flow rate=21; tunnel leads to valve II",
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

Valve = namedtuple("Valve", ["rate", "neighbors"])


def get_valves(inputs:List[str]) -> Dict[str,Valve]:

    """Docstring"""

    valves = {}
    for line in inputs:
        line = line.split(" ", maxsplit=9)
        name = line[1]
        rate = int(line[4].split("=")[1][:-1])
        neighbors = line[9].split(", ")
        valves[name] = Valve(rate, neighbors)

    # print(valves["AA"])
    # print(valves["KP"])

    return valves


def shortest_path(start: str, end: str, valves:Dict[str, Tuple[int, List[str]]]) -> List[str]:

    """Docstring"""

    shortest = []
    paths = defaultdict(list)
    paths[0] = [[start]]
    length = 0
    while len(shortest) == 0:
        for path in paths[length]:
            terminus = valves[path[-1]]
            for neighbor in terminus.neighbors:
                if neighbor not in path:
                    appended = path + [neighbor]
                    if neighbor == end:
                        shortest = appended
                        break
                    paths[length+1].append(appended)
            if len(shortest) != 0:
                break
        length += 1

    return shortest


def value_of(path: List[str], time: int, unopened: Set[str], valves:Dict[str, Tuple[int, List[str]]]) -> int:

    """Docstring"""

    assert (terminus := path[-1]) in unopened

    intermediates:Set = set(path) & unopened
    intermediates.remove(terminus)

    best_value = 0
    valves_on = set()
    for count in range(len(intermediates)+1):
        for on in combinations(intermediates, count):
            on = set(on)
            on.add(terminus)
            elapsed = 0
            value = 0
            for valve in path:
                if valve in on:
                    elapsed += 1
                    value += valves[valve].rate * (time - elapsed)
                elapsed += 1
            if value > best_value:
                best_value = value
                valves_on = set(on)

    return best_value, valves_on, elapsed


def part1() -> None:

    """Docstring"""

    inputs = get_inputs(example=False)
    valves = get_valves(inputs)

    unopened = [key for key, value in valves.items() if value.rate > 0]
    print(f"{unopened=}")

    # tstart = datetime.now()
    # # options = [shortest_path("AA", valve, valves) for valve in unopened]
    # options = []
    # for valve in unopened:
    #     print(f"{valve}...", end="")
    #     shortest = shortest_path("AA", valve, valves)
    #     print(f"{shortest}")
    #     options.append(shortest)
    # tfinish = datetime.now()
    # print(f"{tfinish-tstart} to calculate shortest paths")
    # # print(f"{options=}")

    # # for path in options:
    # #     print(f"unopened valves in {path} = {len(set(path) & set(unopened))}")

    # longest = max(map(len, options))
    # longest = list(filter(lambda o:len(o) == longest, options))[0]

    # value = value_of(longest, 30, set(unopened), valves)
    # print(f"Value of {longest}, 30, {set(unopened)}, ...valves... = {value}")

    ##########

    # unopened = set([key for key in valves if valves[key].rate > 0])
    # unopened = set(unopened)
    # best_path = ["AA"]
    # best_value = 0
    # remaining = 30

    # while remaining > 0:

    #     next_path = []
    #     next_value = 0
    #     next_on = set()
    #     next_elapsed = 0

    #     for option in [shortest_path(best_path[-1], valve, valves) for valve in unopened]:
    #         value, on, elapsed = value_of(option, remaining, unopened, valves)
    #         if (value > next_value) and (elapsed <= remaining):
    #             next_path = option
    #             next_value = value
    #             next_on = on
    #             next_elapsed = elapsed

    #     best_path += next_path[1:]
    #     best_value += next_value
    #     unopened -= next_on
    #     remaining -= next_elapsed

    #     if next_elapsed == 0:   # didn't find any valid candidates
    #         break

    #     if len(unopened) == 0:  # opened all available useful valves
    #         break

    # print(f"{best_path=}")
    # print(f"{best_value=}") # 1840 is too low
    # print(f"{remaining=}")

    distances = np.zeros((len(unopened)+1,len(unopened)+1), np.uint32)

    tstart = datetime.now()
    for i, start in enumerate(["AA"] + unopened):
        for j, dest in enumerate(["AA"] + unopened):
            if j <= i:
                continue
            distances[i,j] = distances[j,i] = len(shortest_path(start, dest, valves))
    tfinish = datetime.now()

    print(f"Calculated distance matrix in {tfinish-tstart}")

    return

def part2() -> None:

    """Docstring"""

    # inputs = get_inputs()

    # return


if __name__ == "__main__":
    main(True, False)
