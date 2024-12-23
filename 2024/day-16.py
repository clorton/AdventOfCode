from pathlib import Path
# import re

import numpy as np

with (Path(__file__).parent / "day-16.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

verbose = False

# Start at "S" facing east.

# lines = [
#     "###############",
#     "#.......#....E#",
#     "#.#.###.#.###.#",
#     "#.....#.#...#.#",
#     "#.###.#####.#.#",
#     "#.#.#.......#.#",
#     "#.#.#####.###.#",
#     "#...........#.#",
#     "###.#.#####.#.#",
#     "#...#.....#.#.#",
#     "#.#.#.###.#.#.#",
#     "#.....#...#.#.#",
#     "#.###.#.#.#.#.#",
#     "#S..#.....#...#",
#     "###############",
# ]

# 7036 = 7 turns and 36 steps
# 45 tiles on one of the best routes

# lines = [
#     "#################",
#     "#...#...#...#..E#",
#     "#.#.#.#.#.#.#.#.#",
#     "#.#.#.#...#...#.#",
#     "#.#.#.#.###.#.#.#",
#     "#...#.#.#.....#.#",
#     "#.#.#.#.#.#####.#",
#     "#.#...#.#.#.....#",
#     "#.#.#####.#.###.#",
#     "#.#.#.......#...#",
#     "#.#.###.#####.###",
#     "#.#.#...#.....#.#",
#     "#.#.#.#####.###.#",
#     "#.#.#.........#.#",
#     "#.#.#.#########.#",
#     "#S#.............#",
#     "#################",
# ]

# 11048 = 11 turns and 48 steps
# 64 tiles on one of the best routes


WALL = ord("#")
SPACE = ord(".")
START = ord("S")
END = ord("E")

maze = np.array([[ord(c) for c in line] for line in lines])

# for row in maze:
#     print("".join([chr(c) for c in row]))

dirs = {
    (0, 1): "v",
    (1, 0): ">",
    (0, -1): "^",
    (-1, 0): "<",
}

def solve(maze):
    ry, rx = np.where(maze == START)
    rx, ry = rx[0], ry[0]

    cost = [[None for _ in range(maze.shape[1])] for _ in range(maze.shape[0])]
    consider = [(rx, ry, 1, 0, 0, 0)]  # x, y, dx, dy, turns, steps
    while consider:
        # consider = sorted(consider, key=lambda x: 1000 * x[4] + x[5])
        cx, cy, cdx, cdy, cturns, csteps = consider.pop(0)
        for p in [-1, 0, 1]:
            rotation = complex(cdx, cdy) * (complex(0, 1) ** p)
            dx, dy = int(rotation.real), int(rotation.imag)
            turns = cturns + abs(p)
            testx, testy = cx + dx, cy + dy
            steps = csteps + 1
            score = 1000 * turns + steps
            if maze[testy, testx] == WALL:
                continue
            if maze[testy, testx] == SPACE:
                if cost[testy][testx] is None:
                    cost[testy][testx] = score
                    consider.append((testx, testy, dx, dy, turns, steps))
                else:
                    if score < cost[testy][testx]:
                        cost[testy][testx] = score
                        consider.append((testx, testy, dx, dy, turns, steps))
            if maze[testy, testx] == END:
                print(f"Found route to the end with cost {score}.")
                if cost[testy][testx] is None:
                    cost[testy][testx] = score
                else:
                    if score < cost[testy][testx]:
                        cost[testy][testx] = score

    # for row in cost:
    #     for col in row:
    #         print("*" if col is not None else " ", end="")
    #     print()

    ey, ex = np.where(maze == END)
    ex, ey = ex[0], ey[0]

    if cost[ey][ex] is not None:
        print(f"Best route to the end costs {cost[ey][ex]}.")
    else:
        print("Failed to find the end.")

    return cost[ey][ex]

best = solve(maze)

from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])
Vector = namedtuple("Vector", ["dx", "dy"])
Candidate = namedtuple("Candidate", ["pos", "dir", "turns", "steps", "parent"])

vecidx = {
    (0, 1): 0,
    (1, 0): 1,
    (0, -1): 2,
    (-1, 0): 3,
}

def solve2(maze, best):
    solutions = []
    # cost to _exit_ is not the same as cost to _enter_ so keep
    # track of costs for each incoming direction
    costs = np.full((maze.shape[0], maze.shape[1], 4), np.inf)
    ys, xs = np.where(maze == START)
    sx, sy = xs[0], ys[0]
    consider = [Candidate(Position(sx, sy), Vector(1, 0), 0, 0, None)]
    while consider:

        if len(consider) % 100 == 0:
            print(f"Considering {len(consider)} candidates.\r", end="")

        candidate = consider.pop(0)

        cx, cy = candidate.pos
        if maze[cy, cx] == WALL:
            continue
        if maze[cy, cx] == END:
            solutions.append(candidate)
            continue

        if candidate.turns*1000 + candidate.steps >= best:
            continue

        iv = vecidx[candidate.dir]
        if (cost:= candidate.turns*1000 + candidate.steps) > costs[cy, cx, iv]:
            continue
        costs[cy, cx, iv] = cost

        for p in [-1, 0, 1]:
            rotation = complex(candidate.dir.dx, candidate.dir.dy) * (complex(0, 1) ** p)
            dx, dy = int(rotation.real), int(rotation.imag)
            turns = candidate.turns + abs(p)
            steps = candidate.steps + 1
            testx, testy = cx + dx, cy + dy
            consider.append(Candidate(Position(testx, testy), Vector(dx, dy), turns, steps, candidate))

    print()

    return solutions

s = solve2(maze, best)

minimum = min(map(lambda c: c.turns*1000+c.steps, s))
print(f"Minimum cost is {minimum}.")
filtered = list(filter(lambda c: c.turns*1000+c.steps == minimum, s))
print(f"Number of routes with minimum cost: {len(filtered)}.")
# viz = np.array(maze)
tiles = set()
for route in filtered:
    while route is not None:
        # viz[route.pos.y, route.pos.x] = ord(dirs[(route.dir.dx, route.dir.dy)]) # ord("O")
        tiles.add(route.pos)
        route = route.parent
# for row in viz:
#     print("".join([chr(c) for c in row]))
print(f"Number of tiles on the shortest route(s): {len(tiles)}.")

print("Done.")
