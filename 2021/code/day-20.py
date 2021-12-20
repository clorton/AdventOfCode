#! /usr/bin/env python3

from pathlib import Path

import numpy as np

with Path("../inputs/20.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

splines = [
    "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#",
    "",
    "#..#.",
    "#....",
    "##..#",
    "..#..",
    "..###",
]

table = str.maketrans(".#", "01")
enhancement = np.array(list(map(int, list(lines[0].translate(table)))), dtype=np.uint32)
start = np.array([list(map(int, list(line.translate(table)))) for line in lines[2:]], dtype=np.uint32)
kernel = np.array([[256, 128, 64], [32, 16, 8], [4, 2, 1]], dtype=np.uint32)


def process_image(pre, mapping, step):

    h, w = pre.shape

    if step == 0:
        fill = 0
    else:
        fill = mapping[9*mapping[0]]
        if step % 2 == 0:
            fill = mapping[9*fill]

    work = np.full((h+6, w+6), fill, dtype=np.uint32)
    work[3:h+3, 3:w+3] = pre

    post = np.zeros((h+4, w+4), dtype=np.uint32)

    for y in range(h+4):
        for x in range(w+4):
            post[y, x] = mapping[(work[y:y+3, x:x+3] * kernel).sum()]

    return post


image = start
for step in range(2):
    image = process_image(image, enhancement, step+1)

num_lit = np.count_nonzero(image)
print(f"{num_lit=}")   # 6276 is too high

image = start
for step in range(50):
    image = process_image(image, enhancement, step+1)

num_lit = np.count_nonzero(image)
print(f"{num_lit=}")   # 6276 is too high

pass
