#! /usr/bin/env python3

from collections import Counter
from functools import cmp_to_key
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

hands = [list(line.split()) for line in input]
hands = [(list(cards), int(bid)) for cards, bid in hands]

kinds = {
    6 : {5:1},      # five of a kind
    5 : {4:1, 1:1}, # four of a kind
    4 : {3:1, 2:1}, # full house
    3 : {3:1, 1:2}, # three of a kind
    2 : {2:2, 1:1}, # two pair
    1 : {2:1, 1:3}, # one pair
    0 : {1:5}       # high card
}

names = {
    6 : "five of a kind",
    5 : "four of a kind",
    4 : "full house",
    3 : "three of a kind",
    2 : "two pair",
    1 : "one pair",
    0 : "high card"
}

scored = []
for cards, bid in hands:
    counts = Counter(Counter(cards).values())
    value = list(filter(lambda kvp: kvp[1] == counts, kinds.items()))[0][0]
    scored.append((cards, bid, value))

ranks = { c:i+2 for i,c in enumerate("23456789TJQKA") }

def compare(a, b):
    if a[2] != b[2]:    # compare hand values
        return [-1,1][a[2] >= b[2]]
    for a, b in zip(a[0], b[0]):
        if a == b:
            continue
        return [-1,1][ranks[a] >= ranks[b]]
    raise RuntimeError
    
scored = sorted(scored, key=cmp_to_key(compare))

winnings = 0
for i, (_, bid, _) in enumerate(scored):
    winnings += bid * (i+1)

print(f"{winnings=}")

def score(cards):
    counts = Counter(Counter(cards).values())
    value = list(filter(lambda kvp: kvp[1] == counts, kinds.items()))[0][0]
    return value

def variants(cards):
    if cards == ["J","J","J","J","J"]:
        return 6
    if not "J" in cards:
        return score(cards)
    test = list(cards)
    i = test.index("J")
    best =  0
    for substitute in (set(test)-set("J")):
        test[i] = substitute
        best = max(best, variants(test))
    return best

print(f"{hands[0][0]} {names[variants(hands[0][0])]}")
print(f"{hands[1][0]} {names[variants(hands[1][0])]}")
print(f"{hands[2][0]} {names[variants(hands[2][0])]}")
print(f"{hands[3][0]} {names[variants(hands[3][0])]}")
print(f"{hands[4][0]} {names[variants(hands[4][0])]}")

rescored = []
for cards, bid in hands:
    value = variants(cards)
    rescored.append((cards, bid, value))

jranks = { c:i+1 for i,c in enumerate("J23456789T?QKA") }

def compare2(a, b):
    if a[2] != b[2]:    # compare hand values
        return [-1,1][a[2] >= b[2]]
    for a, b in zip(a[0], b[0]):
        if a == b:
            continue
        return [-1,1][jranks[a] >= jranks[b]]
    raise RuntimeError
    
rescored = sorted(rescored, key=cmp_to_key(compare2))

winnings = 0
for i, (_, bid, _) in enumerate(rescored):
    winnings += bid * (i+1)

print(f"{winnings=}")

pass
