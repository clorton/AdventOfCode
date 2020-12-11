#!/usr/bin/env python3

from collections import namedtuple


Node = namedtuple('Node', ['parent', 'child'])


def main():

    with open('day-06.txt', "r") as file:
        lines = file.readlines()

    # lines = [
    #     "COM)B",
    #     "B)C",
    #     "C)D",
    #     "D)E",
    #     "E)F",
    #     "B)G",
    #     "G)H",
    #     "D)I",
    #     "E)J",
    #     "J)K",
    #     "K)L",
    #     "K)YOU",
    #     "I)SAN"
    # ]

    lines = [line.strip() for line in lines]
    inputs = [Node(*entry.split(')')) for entry in lines]

    masses = {"COM": None}
    for entry in inputs:
        parent = entry.parent
        child = entry.child
        if child not in masses:
            masses[child] = parent
        else:
            raise RuntimeError(f"mass {child} already in the map ({masses[child]})")

    total = 0
    for mass in masses.keys():
        count = 0
        while masses[mass] is not None:
            count += 1
            mass = masses[mass]
        total += count

    print(f"Total orbits is {total}")

    # Part 2

    location = 'YOU'
    path = []
    while masses[location] is not None:
        path.append(masses[location])
        location = masses[location]

    your_path = ":".join(reversed(path))

    location = 'SAN'
    path = []
    while masses[location] is not None:
        path.append(masses[location])
        location = masses[location]

    santa_path = ":".join(reversed(path))

    print(f"Your path is    {your_path}")
    print(f"Santa's path is {santa_path}")

    your_path = list(reversed(your_path.split(":")))
    santa_path = list(reversed(santa_path.split(":")))

    while your_path[-1] == santa_path[-1]:
        your_path.pop(-1)
        santa_path.pop(-1)

    print(f"Transfers = {len(your_path)+len(santa_path)}")

    return


if __name__ == "__main__":
    main()
