#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from math import lcm
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

instructions = input[0]

Node = namedtuple("Node", ["left", "right"])

nodes = [ (line.split(" = ")) for line in input[2:] ]
nodes = [ [node] + list(children[1:-1].split(", ")) for node, children in nodes ]
nodes = { node: Node(left, right) for node, left, right in nodes }

node = "AAA"
steps = 0
while node != "ZZZ":
    node = nodes[node].left if instructions[steps % len(instructions)] == "L" else nodes[node].right
    steps += 1

print(f"{steps=}")

ghosts = list(filter(lambda k: k.endswith("A"), nodes.keys()))
zees = [[] for _ in range(len(ghosts))]

steps = 0
while not all(map(lambda g: g.endswith("Z"), ghosts)):
    left = instructions[steps % len(instructions)] == "L"
    ghosts = [ nodes[node].left if left else nodes[node].right for node in ghosts ]
    steps += 1
    found = False
    for i, node in enumerate(ghosts):
        if node.endswith("Z"):
            zees[i].append(steps)
            found = True
    if found:
        # print(f"{ghosts}: {zees}")
        if all(zees):
            print(f"{lcm(*[z[0] for z in zees])=}")
            break

pass
