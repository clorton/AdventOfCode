#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-21.txt").read_text()

# text = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)"""

lines = text.split("\n")
lines = [line.replace(")", "") for line in lines]
lines = [line.split(" (contains ") for line in lines]
for line in lines:
    line[0] = set(line[0].split(" "))
    line[1] = set(line[1].split(", "))

options = {}
universe = set()
for ingredients, allergens in lines:
    universe.update(ingredients)
    for allergen in allergens:
        if allergen not in options:
            options[allergen] = set(ingredients)
        else:
            options[allergen] &= ingredients

possibilities = set()
for allergen, ingredients in options.items():
    possibilities.update(ingredients)

impossibilities = universe - possibilities
count = 0
for ingredients, allergens in lines:
    count += len(ingredients & impossibilities)

print(f"impossible ingredients appear {count} times")

# part 1


# part 2
biggest = max([len(ingredients) for ingredients in options.values()])
while biggest > 1:
    for allergen, ingredients in options.items():
        if len(ingredients) == 1:
            for x, y in options.items():
                if x != allergen:
                    y -= ingredients
    biggest = max([len(ingredients) for ingredients in options.values()])

alpha = sorted(options.keys())
ingredients = [list(options[key])[0] for key in alpha]
result = ",".join(ingredients)

print(f"Canonical list is '{result}'")

print(".oO( done )")
