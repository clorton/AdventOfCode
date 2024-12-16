from pathlib import Path
# import re

import numpy as np

with (Path(__file__).parent / "day-16.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

verbose = False

# Start at "S" facing east.

"""
lines = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############",
]

# 7036 = 7 turns and 36 steps
# 45 tiles on one of the best routes
"""

"""lines = [
    "#################",
    "#...#...#...#..E#",
    "#.#.#.#.#.#.#.#.#",
    "#.#.#.#...#...#.#",
    "#.#.#.#.###.#.#.#",
    "#...#.#.#.....#.#",
    "#.#.#.#.#.#####.#",
    "#.#...#.#.#.....#",
    "#.#.#####.#.###.#",
    "#.#.#.......#...#",
    "#.#.###.#####.###",
    "#.#.#...#.....#.#",
    "#.#.#.#####.###.#",
    "#.#.#.........#.#",
    "#.#.#.#########.#",
    "#S#.............#",
    "#################",
]

# 11048 = 11 turns and 48 steps
# 64 tiles on one of the best routes
"""

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

import hashlib

def solve2(maze, best):
    ry, rx = np.where(maze == START)
    rx, ry = rx[0], ry[0]

    max_steps = best % 1000
    max_turns = best // 1000

    seen = set()

    solutions = []
    consider = [(rx, ry, 1, 0, 0, 0, {(rx, ry)})]  # x, y, dx, dy, turns, steps, tiles
    iterations = 0
    w, h = 25, -25
    while consider:
        iterations += 1
        if iterations % 100 == 0:
            print(f"{len(consider)=}", end="\r")
        cx, cy, cdx, cdy, cturns, csteps, ctiles = consider.pop(0)
        # if cx == 17 and cy == 128:
        #     ...
        if True:
            p = np.zeros_like(maze, dtype=np.uint8)
            for x, y in ctiles:
                p[y, x] = 1
            d = hashlib.sha256(p.tobytes()).hexdigest()
            if d in seen:
                ...
            seen.add(d)
        #     for row in p[h:,:w]:
        #         print("".join(map(str, row)))
        #     print()
        #     ...
        for p in [-1, 0, 1]:
            rotation = complex(cdx, cdy) * (complex(0, 1) ** p)
            dx, dy = int(rotation.real), int(rotation.imag)
            turns = cturns + abs(p)
            if turns > max_turns:
                # print("x", end="")
                continue
            testx, testy = cx + dx, cy + dy
            steps = csteps + 1
            if steps > max_steps:
                # print("x", end="")
                continue
            score = 1000 * turns + steps
            if maze[testy, testx] == WALL:
                continue
            if (maze[testy, testx] == SPACE) and ((testx, testy) not in ctiles):
                # print("+", end="")
                consider.append((testx, testy, dx, dy, turns, steps, ctiles | {(testx, testy)}))
            if (maze[testy, testx] == END) and ((testx, testy) not in ctiles):
                print(f"\nFound the end in {score} steps with {len(ctiles) + 1} tiles.")
                solutions.append((score, ctiles | {(testx, testy)}))

    print()

    print(f"Found {len(solutions)} solutions.")
    minimum = min(solutions, key=lambda x: x[0])[0]
    print(f"Best solutions cost {minimum}.")
    totaltiles = set()
    for solution in solutions:
        cost, tiles = solution
        if cost == minimum:
            totaltiles.update(tiles)

    print(f"Total tiles: {len(totaltiles)}.")

    return

solve2(maze, best)

print("Done.")
