from pathlib import Path

import numpy as np

with (Path(__file__).parent / "day-12.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "RRRRIICCFF",
#     "RRRRIICCCF",
#     "VVRRRCCFFF",
#     "VVRCCCJFFF",
#     "VVVVCJJCFE",
#     "VVIVCCJJEE",
#     "VVIIICJJEE",
#     "MIIIIIJJEE",
#     "MIIISIJEEE",
#     "MMMISSJEEE",
# ]

"""
A region of R plants with price 12 * 18 = 216.
A region of I plants with price 4 * 8 = 32.
A region of C plants with price 14 * 28 = 392.
A region of F plants with price 10 * 18 = 180.
A region of V plants with price 13 * 20 = 260.
A region of J plants with price 11 * 20 = 220.
A region of C plants with price 1 * 4 = 4.
A region of E plants with price 13 * 18 = 234.
A region of I plants with price 14 * 22 = 308.
A region of M plants with price 5 * 12 = 60.
A region of S plants with price 3 * 8 = 24.
So, it has a total price of 1930.
"""

plants = np.array([list(map(ord, list(line))) for line in lines])
visited = np.full_like(plants, -1)
from collections import defaultdict, namedtuple
Plot = namedtuple("Plot", ["area", "perimeter"])
plots = defaultdict(lambda : Plot(area=0, perimeter=0))

def test(x, y, plants, visited):
    results = []
    perimeter = 4
    plant = plants[y, x]
    for dx, dy in [(0,-1), (1,0), (0,1), (-1,0)]:
        tx, ty = x+dx, y+dy
        if (0 <= tx) and (tx < plants.shape[1]) and (0 <= ty) and (ty < plants.shape[0]):
            if (plants[ty, tx] == plant):
                perimeter -= 1
                if (visited[ty, tx] == -1):
                    results.append((tx, ty))

    return results, perimeter


plot = 0
for y in range(plants.shape[0]):
    for x in range(plants.shape[1]):
        if visited[y, x] == -1:
            totest = {(x, y)}
            while totest:
                tx, ty = totest.pop()
                # print(f"Testing {(tx, ty)}...", end="")
                visited[ty, tx] = plot
                results, perimeter = test(tx, ty, plants, visited)
                # print(f"perimeter = {perimeter}")
                plots[plot] = Plot(plots[plot].area + 1, plots[plot].perimeter + perimeter)
                totest.update(results)
            plot += 1

total = 0
for id, (area, perimeter) in plots.items():
    print(f"Plot {id} = {area} x {perimeter} = {area*perimeter}")
    total += area * perimeter

print(f"Total = {total}")

"""
A region of R plants with price 12 * 10 = 120.
A region of I plants with price 4 * 4 = 16.
A region of C plants with price 14 * 22 = 308.
A region of F plants with price 10 * 12 = 120.
A region of V plants with price 13 * 10 = 130.
A region of J plants with price 11 * 12 = 132.
A region of C plants with price 1 * 4 = 4.
A region of E plants with price 13 * 8 = 104.
A region of I plants with price 14 * 16 = 224.
A region of M plants with price 5 * 6 = 30.
A region of S plants with price 3 * 6 = 18.
Adding these together produces its new total price of 1206.
"""

Edge = namedtuple("Edge", ["x", "y", "edge"])

dirtoedge = {
    (0,-1): "h1",
    (1, 0): "v2",
    (0, 1): "h2",
    (-1,0): "v1"
}

def test2(x, y, plants, visited):
    results = []
    edges = set()
    perimeter = 4
    plant = plants[y, x]
    for dx, dy in [(0,-1), (1,0), (0,1), (-1,0)]:
        tx, ty = x+dx, y+dy
        if (0 <= tx) and (tx < plants.shape[1]) and (0 <= ty) and (ty < plants.shape[0]):
            if (plants[ty, tx] == plant):
                perimeter -= 1
                if (visited[ty, tx] == -1):
                    results.append((tx, ty))
            else:
                edges.add(Edge(x, y, dirtoedge[(dx, dy)]))
        else:
            edges.add(Edge(x, y, dirtoedge[(dx, dy)]))

    return results, perimeter, edges

def mergeedges(edges):
    merged = set()
    while edges:
        e1 = sorted(edges)[0]
        edges.remove(e1)
        unmerged = set()
        for e2 in sorted(edges):
            # if (e1.x1 == e1.x2) and (e2.x1 == e2.x2) and (e1.x1 == e2.x2):      # both vertical
            #     if (e1.y2 == e2.y1) or (e2.y2 == e1.y1):
            #         e1 = Edge(e1.x1, min(e1.y1, e2.y1), e1.x2, max(e1.y2, e2.y2))
            #     else:
            #         unmerged.add(e2)
            # elif (e1.y1 == e1.y2) and (e2.y1 == e2.y2) and (e1.y1 == e2.y2):   # both horizontal
            #     if (e1.x2 == e2.x1) or (e2.x2 == e1.x1):
            #         e1 = Edge(min(e1.x1, e2.x1), e1.y1, max(e1.x2, e2.x2), e1.y2)
            #     else:
            #         unmerged.add(e2)
            # else:
            #     unmerged.add(e2)
            if e1.edge == e2.edge:
                if e1.edge[0] == "h":   # horizontal
                    if (e2.y == e1.y) and (e2.x == (e1.x + 1)):
                        e1 = Edge(e2.x, e1.y, e1.edge)
                    else:
                        unmerged.add(e2)
                else:   # vertical
                    if (e2.x == e1.x) and (e2.y == (e1.y + 1)):
                        e1 = Edge(e1.x, e2.y, e1.edge)
                    else:
                        unmerged.add(e2)
            else:
                unmerged.add(e2)
        merged.add(e1)
        edges = unmerged

    return merged

visited = np.full_like(plants, -1)
Plot2 = namedtuple("Plot2", ["area", "perimeter", "edges"])
plots2 = defaultdict(lambda : Plot2(area=0, perimeter=0, edges=set()))
plot = 0
for y in range(plants.shape[0]):
    for x in range(plants.shape[1]):
        if visited[y, x] == -1:
            totest = {(x, y)}
            while totest:
                tx, ty = totest.pop()
                # print(f"Testing {(tx, ty)}...", end="")
                visited[ty, tx] = plot
                results, perimeter, edges = test2(tx, ty, plants, visited)
                # print(f"perimeter = {perimeter}")
                areap = plots2[plot].area + 1
                perimeterp = plots2[plot].perimeter + perimeter
                edgesp = plots2[plot].edges
                edgesp.update(edges)
                plots2[plot] = Plot2(areap, perimeterp, edgesp)
                totest.update(results)
            plots2[plot] = Plot2(plots2[plot].area, plots2[plot].perimeter, mergeedges(plots2[plot].edges))
            plot += 1

total = 0
for id, (area, perimeter, edges) in plots2.items():
    print(f"Plot {id} = {area} x {len(edges)} = {area*len(edges)}")
    total += area * len(edges)

print(f"Total = {total}")

print("Done.")
