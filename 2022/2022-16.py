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

    distances = np.zeros((len(unopened)+1,len(unopened)+1), np.uint32)
    states = np.zeros(len(unopened)+1, np.uint32)
    values = np.zeros(len(unopened)+1, np.uint32)

    tstart = datetime.now()
    for i, start in enumerate(["AA"] + unopened):
        values[i] = valves[start].rate
        for j, dest in enumerate(["AA"] + unopened):
            if j <= i:
                continue
            distances[i,j] = distances[j,i] = (len(shortest_path(start, dest, valves)) - 1)
    tfinish = datetime.now()

    print(f"Calculated distance matrix in {tfinish-tstart}")

    # Starting at AA, consider all valves reachable within remaining time
    # Cutting off search when remaining time = 0 should make depth first search tractable.

    def best_option(start:int, states:np.ndarray, remaining:int, distances:np.ndarray, values:np.ndarray) -> int:

        value = values[start] * remaining
        best = 0
        for destination in np.nonzero((distances[start,:] < remaining) & (states != 1))[0]:
            states[destination] = 1
            remaining -= distances[start,destination] + 1
            best = max(best, best_option(destination, states, remaining, distances, values))
            remaining += distances[start,destination] + 1
            states[destination] = 0

        return value + best

    states[0] = 1    # Consider valve "AA" turned on.
    best = best_option(0, states, 30, distances, values)
    print(f"Part 1: best option releases {best} pounds of pressure.")

    return

def part2() -> None:

    """Docstring"""

    inputs = get_inputs(example=True)
    valves = get_valves(inputs)

    unopened = [key for key, value in valves.items() if value.rate > 0]
    print(f"{unopened=}")

    distances = np.zeros((len(unopened)+1,len(unopened)+1), np.uint32)
    states= np.zeros(len(unopened)+1, np.uint32)
    values = np.zeros(len(unopened)+1, np.uint32)

    tstart = datetime.now()
    for i, start in enumerate(["AA"] + unopened):
        values[i] = valves[start].rate
        for j, dest in enumerate(["AA"] + unopened):
            if j <= i:
                continue
            distances[i,j] = distances[j,i] = (len(shortest_path(start, dest, valves)) - 1)
    tfinish = datetime.now()

    print(f"Calculated distance matrix in {tfinish-tstart}")

    # Starting at AA, consider all valves reachable within remaining time
    # Cutting off search when remaining time = 0 should make depth first search tractable.

    def best_option2(location:int, states:np.ndarray, remaining:int, distances:np.ndarray, values:np.ndarray) -> int:

        value = values[location] * remaining
        best = 0
        path = [location]
        for destination in np.nonzero((distances[location,:] < remaining) & (states != 1))[0]:
            states[destination] = 1
            remaining -= distances[location,destination] + 1
            test, route = best_option2(destination, states, remaining, distances, values)
            if test > best:
                best = test
                path = [location] + route
            remaining += distances[location,destination] + 1
            states[destination] = 0

        return value + best, path

    states[0] = 1    # Consider valve "AA" turned on.
    human, route = best_option2(0, states, 26, distances, values)
    for valve in route:
        states[valve] = 1
    elephant, path = best_option2(0, states, 26, distances, values)
    print(f"Part 2: human releases {human} pounds of pressure on route {route}.")
    print(f"Part 2: elephant releases {elephant} pounds of pressure on route {path}.")
    print(f"Part 2: total of {human+elephant} pounds of pressure released")

    # BTW, this does _not_ return the correct answer for the example data.

    return

if __name__ == "__main__":
    main(False, True)
