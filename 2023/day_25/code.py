#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from pathlib import Path
from math import prod

import networkx as nx
import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

# graph = defaultdict(set)
graph = nx.Graph()
for i in tqdm(range(len(input))):
    line = input[i]
    component, connections = line.split(": ")
    connections = connections.split(" ")
    for connection in connections:
        # graph[component].add(connection)
        # graph[connection].add(component)
        graph.add_edge(component, connection)

import matplotlib.pyplot as plt
figure = plt.figure(figsize=(16, 16))
nx.draw(graph, with_labels=True)
figure.savefig("graph.png")

# cut mxd/glz
graph.remove_edge("mxd", "glz")
# cut brd/clb
graph.remove_edge("brd", "clb")
# cut bbz/jxd
graph.remove_edge("bbz", "jxd")

figure = plt.figure(figsize=(16, 16))
nx.draw(graph, with_labels=True)
figure.savefig("graphminus.png")

# get sizes of the disconnected components
sizes = [len(c) for c in nx.connected_components(graph)]
print(f"{sizes=}")
print(f"{prod(sizes)=}")

pass
