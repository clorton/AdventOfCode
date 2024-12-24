from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "day-23.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "kh-tc",
#     "qp-kh",
#     "de-cg",
#     "ka-co",
#     "yn-aq",
#     "qp-ub",
#     "cg-tb",
#     "vc-aq",
#     "tb-ka",
#     "wh-tc",
#     "yn-cg",
#     "kh-ub",
#     "ta-co",
#     "de-co",
#     "tc-td",
#     "tb-wq",
#     "wh-td",
#     "ta-ka",
#     "td-qp",
#     "aq-cg",
#     "wq-ub",
#     "ub-vc",
#     "de-ta",
#     "wq-aq",
#     "wq-vc",
#     "wh-yn",
#     "ka-de",
#     "kh-ta",
#     "co-tc",
#     "wh-qp",
#     "tb-vc",
#     "td-yn",
# ]

from collections import defaultdict
connections = defaultdict(set)

for line in lines:
    a, b = line.split("-")
    connections[a].add(b)
    connections[b].add(a)

from itertools import combinations

threes = defaultdict(set)
for k, v in connections.items():
    for b, c in combinations(v, 2):
        threes[",".join(sorted([k, b, c]))].add(k)

triples = {k:threes[k] for k in sorted(filter(lambda k: len(threes[k]) == 3, threes.keys()))}

hasat = {k:v for k, v in triples.items() if any(filter(lambda e: e.startswith("t"), v))}

print(f"len(hasat) = {len(hasat)}")

# Part 2

"""
import networkx as nx

# Create a sample graph
G = nx.Graph()
G.add_edges_from([(a, b) for a, b in map(lambda l: l.split("-"), lines)])

# Find all cliques in the graph
all_cliques = list(nx.find_cliques(G))

# Find the largest clique
largest_clique = max(all_cliques, key=len)

print("Largest clique:", ",".join(sorted(largest_clique)))
"""

c = defaultdict(set)
for k, v in connections.items():
    for l in range(1, len(v)+1):
        for combo in combinations(v, l):
            c[",".join(sorted([k] + list(combo)))].add(k)

f = {k:v for k,v in c.items() if ",".join(sorted(v)) == k}
maximum = max(map(lambda k: len(k), f.keys()))
m = {k:v for k,v in f.items() if len(k) == maximum}
print(m)

print("Done.")
