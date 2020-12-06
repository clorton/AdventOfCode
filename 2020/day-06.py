#! /usr/bin/env python3

from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-06.txt").read_text()

groups = text.split("\n\n")

# part 1
count = 0
for group in groups:
    yeses = set()
    for answers in group.split("\n"):
        yeses.update(list(answers))
    count += len(yeses)

print(f"Total count is {count}.")


# part 2
count = 0
for group in groups:
    responses = group.split("\n")
    yeses = set(list(responses[0]))
    for answers in responses[1:]:
        yeses = yeses & set(list(answers))
    count += len(yeses)

print(f"Total count is {count}.")

print("done")
