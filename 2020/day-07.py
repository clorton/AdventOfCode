#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-07.txt").read_text()
rules = text.split("\n")

Spec = namedtuple("Spec", ["count", "type"])

# part 1
rules = [rule.split(" contain ") for rule in rules]
for rule in rules:
    container = rule[0].replace(" bags", "")
    contents = []
    for content in rule[1].split(", "):
        if content.startswith("no"):
            continue
        content = content.replace(".", "")
        content = content.replace(" bags", "")
        content = content.replace(" bag", "")
        temp = content.split(" ", 1)
        contents.append(Spec(int(temp[0]), temp[1]))
    rule[0] = container
    rule[1] = contents

seen = set(["shiny gold"])
targets = ["shiny gold"]
while len(targets):
    target = targets.pop(0)
    for container, contents in rules:
        allowed = set([temp.type for temp in contents])
        if target in allowed and container not in seen:
            targets.append(container)
    seen.update([target])

print(f"{len(seen)-1} bags could contain a shiny gold bag.")

# part 2
rules = {container: contents for container, contents in rules}
cargo = defaultdict(int)


def contents_of(consider):
    global cargo
    for entry in rules[consider]:
        if entry.type in cargo:
            cargo[consider] += entry.count * (1 + cargo[entry.type])
        else:
            cargo[consider] += entry.count * (1 + contents_of(entry.type))
    return cargo[consider]


n = contents_of("shiny gold")

print(f"Shiny gold bags contain {n} other bags.")

print("done")
