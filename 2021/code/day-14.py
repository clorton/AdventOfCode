#! /usr/bin/env python3

from collections import Counter, defaultdict, namedtuple
from datetime import datetime
from pathlib import Path

import numpy as np

with Path("../inputs/14.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

"""
lines = [
    "NNCB",
    "",
    "CH -> B",
    "HH -> N",
    "CB -> H",
    "NH -> C",
    "HB -> C",
    "HC -> B",
    "HN -> C",
    "NN -> C",
    "BH -> H",
    "NC -> B",
    "NB -> B",
    "BN -> B",
    "BB -> N",
    "BC -> B",
    "CC -> N",
    "CN -> C"
]
"""

template = lines[0]
rules = list([line.split(" -> ") for line in lines[2:]])
rules = {rule[0]: rule[1] for rule in rules}


def process(template, rules):
    scratch = np.zeros(len(template) * 2 - 1, dtype=np.dtype('i1'))
    j = 0
    for i in range(0, len(template)-1):
        scratch[j] = ord(template[i])
        scratch[j+1] = ord(rules[template[i:i+2]])
        # scratch[j+2] = ord(template[i+1])
        j += 2
    scratch[j] = ord(template[-1])
    return "".join(map(chr, scratch))


for step in range(10):
    template = process(template, rules)

counts = Counter(list(template))
reverse = {value: key for key, value in counts.items()}
minimum = min(reverse.keys())
maximum = max(reverse.keys())
print(f"{maximum - minimum=}")

# Part 2

seed = defaultdict(int)
for i in range(len(lines[0])-1):
    seed[lines[0][i:i+2]] += 1


def do_step(state, rules):
    next_state = defaultdict(int)
    for dimer, count in state.items():
        trimer = "".join([dimer[0], rules[dimer], dimer[1]])
        next_state[trimer[0:2]] += count
        next_state[trimer[1:3]] += count
    return next_state


for i in range(40):
    seed = do_step(seed, rules)

    counts = defaultdict(int)
    for dimer, count in seed.items():
        counts[dimer[0]] += count   # count just the first atom since the second atom will be the first of another dimer
    counts[lines[0][-1]] += 1       # except the very last atom...

reverse = {value: key for key, value in counts.items()}
minimum = min(reverse.keys())
maximum = max(reverse.keys())
print(f"{maximum - minimum=}")

pass
