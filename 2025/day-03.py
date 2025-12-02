from pathlib import Path

HERE = Path(__file__).parent

with Path(HERE / "day-03.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

actions = [(line[0], int(line[1:])) for line in lines]

print("done")
