#! /usr/bin/env python3

import numpy as np
from pathlib import Path
from functools import reduce
from collections import defaultdict


def get_data():
    text = (Path(__file__).parent.absolute() / "day-20.txt").read_text()
    data = text.split("\n\n")
    tiles = {}
    for entry in data:
        rows = entry.split("\n")
        id = int(rows[0].split(" ")[1][:-1])
        pixels = "".join([str(row) for row in rows[1:]])
        pixels = list(map(lambda x: 1 if x == "#" else 0, pixels))
        tile = np.fromiter(pixels, dtype=np.uint8)
        tiles[id] = np.reshape(tile, (10, 10))

    return tiles


# part 1
def reduction(t, s):
    return (t << 1) + s


def edges_of(tile):

    edges = set()
    edges.update([reduce(reduction, tile[0, :])])
    edges.update([reduce(reduction, tile[0, ::-1])])
    edges.update([reduce(reduction, tile[-1, :])])
    edges.update([reduce(reduction, tile[-1, ::-1])])
    edges.update([reduce(reduction, tile[:, 0])])
    edges.update([reduce(reduction, tile[::-1, 0])])
    edges.update([reduce(reduction, tile[:, -1])])
    edges.update([reduce(reduction, tile[::-1, -1])])

    return edges


def part1(tiles):

    edges = {}
    for id, tile in tiles.items():
        edges[id] = edges_of(tile)

    tile_ids = list(edges.keys())
    matches = defaultdict(set)
    for i, idOne in enumerate(tile_ids):
        for idTwo in tile_ids[i+1:]:
            if len(edges[idOne] & edges[idTwo]) > 0:
                matches[idOne].update([idTwo])
                matches[idTwo].update([idOne])

    product = 1
    for id, partners in matches.items():
        if len(partners) == 2:
            print(f"Tile {id} has 2 matching tiles {partners}.")
            product *= id
            continue
        if len(partners) == 3 or len(partners) == 4:
            continue
        raise RuntimeError(f"Found tile, {id}, with unusual number of partners, {len(partners)} = {partners}")

    print(f"Product of corner tile ids is {product}")

    return edges, matches


t = get_data()
e, m = part1(t)


# part 2
def part2(tiles, edges, matches):

    # Find a corner
    corners = [tile for tile, neighbors in matches.items() if len(neighbors) == 2]
    corner = corners[0]
    count = len(tiles)
    dimension = int(np.sqrt(count))
    layout = np.zeros((dimension, dimension), dtype=np.uint32)

    # top row
    layout[0, 0] = corner
    previous = corner
    current = list(matches[corner])[0]
    for x in range(1, dimension):
        layout[0, x] = current
        neighbor = list(set([tile for tile in matches[current] if len(matches[tile]) < 4]) - set([previous]))[0]
        previous = current
        current = neighbor

    # right side
    for y in range(1, dimension):
        layout[y, -1] = current
        neighbor = list(set([tile for tile in matches[current] if len(matches[tile]) < 4]) - set([previous]))[0]
        previous = current
        current = neighbor

    # left side
    previous = corner
    current = list(matches[corner])[1]
    for y in range(1, dimension):
        layout[y, 0] = current
        neighbor = list(set([tile for tile in matches[current] if len(matches[tile]) < 4]) - set([previous]))[0]
        previous = current
        current = neighbor

    # bottom row
    for x in range(1, dimension):
        layout[-1, x] = current
        neighbor = list(set([tile for tile in matches[current] if len(matches[tile]) < 4]) - set([previous]))[0]
        previous = current
        current = neighbor

    # interior
    for y in range(1, dimension-1):
        for x in range(1, dimension-1):
            north = layout[y-1, x]
            west = layout[y, x-1]
            northwest = layout[y-1, x-1]
            current = list((matches[north] & matches[west]) - set([northwest]))[0]
            layout[y, x] = current

    # orient top left corner (layout[0, 0])
    tile = tiles[layout[0, 0]]
    east = layout[0, 1]
    while True:
        edge = reduce(reduction, tile[:, -1])
        if edge in edges[east]:
            break
        tile = np.rot90(tile)
    # top left corner matches east neighbor
    edge = reduce(reduction, tile[-1, :])   # bottom edge
    south = layout[1, 0]
    if edge not in edges[south]:
        tile = np.flipud(tile)
        edge = reduce(reduction, tile[-1, :])
        assert edge in edges[south]
    tiles[layout[0, 0]] = tile

    # orient rest of top row
    for x in range(1, dimension):
        anchor = layout[0, x-1]
        match = reduce(reduction, tiles[anchor][:, -1])    # east edge
        east = layout[0, x]
        tile = tiles[east]
        while True:
            edge = reduce(reduction, tile[:, 0])    # west edge
            if edge == match:
                break
            tile = np.flipud(tile)
            edge = reduce(reduction, tile[:, 0])  # west edge
            if edge == match:
                break
            tile = np.rot90(np.flipud(tile))    # undo flip before rotate
        tiles[east] = tile

    # orient remaining rows:
    for y in range(1, dimension):
        for x in range(dimension):
            anchor = layout[y-1, x]
            match = reduce(reduction, tiles[anchor][-1, :])     # south edge
            south = layout[y, x]
            tile = tiles[south]
            while True:
                edge = reduce(reduction, tile[0, :])    # north edge
                if edge == match:
                    break
                tile = np.fliplr(tile)
                edge = reduce(reduction, tile[0, :])    # north edge
                if edge == match:
                    break
                tile = np.rot90(np.fliplr(tile))    # undo flip before rotate
            tiles[south] = tile

    # hardcode some values...
    bitmap = np.zeros((96, 96), dtype=np.uint8)
    for y in range(12):
        for x in range(12):
            bitmap[8*y:8*(y+1), 8*x:8*(x+1)] = tiles[layout[y, x]][1:-1, 1:-1]

    sea_monster = np.zeros((3, 20), dtype=np.uint8)
    sea_monster[0, :] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    sea_monster[1, :] = [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1]
    sea_monster[2, :] = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]

    count = np.sum(sea_monster)
    total = np.sum(bitmap)

    bmp_height, bmp_width = bitmap.shape
    sea_height, sea_width = sea_monster.shape
    for _ in range(4):
        found = 0
        for y in range(bmp_height-sea_height):
            for x in range(bmp_width-sea_width):
                pixels = np.sum(bitmap[y:y+sea_height, x:x+sea_width]*sea_monster)
                found += 1 if pixels == count else 0
        bitmap = np.flipud(bitmap)
        print(f"Found = {found}")
        print(f"Roughess = {total-count*found}") if found > 0 else None
        found = 0
        for y in range(bmp_height-sea_height):
            for x in range(bmp_width-sea_width):
                pixels = np.sum(bitmap[y:y+sea_height, x:x+sea_width]*sea_monster)
                found += 1 if pixels == count else 0
        print(f"Found = {found}")
        print(f"Roughess = {total-count*found}") if found > 0 else None
        bitmap = np.rot90(np.flipud(bitmap))

    print()
    return


part2(t, e, m)
print(".oO( done )")
