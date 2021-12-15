#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from datetime import datetime
from pathlib import Path

import numpy as np

with Path("12.txt").open("r") as handle:
    lines = list([line.strip().split("-") for line in handle.readlines()])

t_start = datetime.now()

"""
lines = [
    "start-A".split("-"),
    "start-b".split("-"),
    "A-c".split("-"),
    "A-b".split("-"),
    "b-d".split("-"),
    "A-end".split("-"),
    "b-end".split("-")
]

lines = [
    "dc-end".split("-"),
    "HN-start".split("-"),
    "start-kj".split("-"),
    "dc-start".split("-"),
    "dc-HN".split("-"),
    "LN-dc".split("-"),
    "HN-end".split("-"),
    "kj-sa".split("-"),
    "kj-HN".split("-"),
    "kj-dc".split("-")
]

lines = [
    "fs-end".split("-"),
    "he-DX".split("-"),
    "fs-he".split("-"),
    "start-DX".split("-"),
    "pj-DX".split("-"),
    "end-zg".split("-"),
    "zg-sl".split("-"),
    "zg-pj".split("-"),
    "pj-he".split("-"),
    "RW-he".split("-"),
    "fs-DX".split("-"),
    "pj-RW".split("-"),
    "zg-RW".split("-"),
    "start-pj".split("-"),
    "he-WI".split("-"),
    "zg-he".split("-"),
    "pj-fs".split("-"),
    "start-RW".split("-")
]
"""

connections = []
for left, right in lines:
    connections.append((left, right)) if (left != "end") and (right != "start") else None
    connections.append((right, left)) if (right != "end") and (left != "start") else None

edges = defaultdict(list)
for start, end in connections:
    edges[start].append(end)

Path = namedtuple("Path", ["sequence", "seen"])
paths = [Path(["start"], ["start"])]
routes = []
while len(paths) > 0:
    path = paths.pop()
    start = path.sequence[-1]
    for end in edges[start]:
        if end == "end":
            sequence = list(path.sequence)
            sequence.append(end)
            seen = set(path.seen)
            seen.update(("end",))
            routes.append(Path(sequence, seen))
        elif end not in path.seen:
            sequence = list(path.sequence)
            sequence.append(end)
            seen = set(path.seen)
            if end.islower():
                seen.update((end,))
            paths.append(Path(sequence, seen))

print(f"Found {len(routes)} routes.")

paths = [Path(["start"], defaultdict(int))]
routes = []
while len(paths) > 0:
    path = paths.pop()
    start = path.sequence[-1]
    for end in edges[start]:
        if end == "end":
            sequence = list(path.sequence)
            sequence.append(end)
            seen = set(path.seen)
            seen.update(("end",))
            routes.append(Path(sequence, seen))
        elif (end not in path.seen) or (path.seen[end] == 0):
            sequence = list(path.sequence)
            sequence.append(end)
            seen = defaultdict(int, path.seen)
            if end.islower():
                seen[end] += 1
            paths.append(Path(sequence, seen))
        elif (end in path.seen) and (path.seen[end] == 1) and (max(path.seen.values()) < 2):
            sequence = list(path.sequence)
            sequence.append(end)
            seen = defaultdict(int, path.seen)
            if end.islower():
                seen[end] += 1
            paths.append(Path(sequence, seen))

t_end = datetime.now()

print(f"Found {len(routes)} routes.")

print(f"{t_end-t_start}")

pass
