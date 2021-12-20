#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from pathlib import Path

import numpy as np

Point = namedtuple("Point", ["x", "y", "z"])
permutations = [
    [0, 1, 2],
    [0, 2, 1],
    [1, 0, 2],
    [1, 2, 0],
    [2, 0, 1],
    [2, 1, 0]
]
Info = namedtuple("Info", ["points", "abs", "mapping"])


def main():

    inputs = get_inputs()

    baseline = process(inputs[0], permutations[0], [1, 1, 1])
    processed = [baseline]
    good = [baseline]
    remaining = set(range(1, len(inputs)))
    while len(good) > 0:
        i = good.pop(0)
        for j in list(remaining):
            for permutation in permutations:
                test = process(inputs[j], permutation, [1, 1, 1])
                shared = list(i.abs & test.abs)
                if len(shared) == 66:

                    distance = shared[0]
                    p1a, p1b = i.mapping[distance]
                    dp1 = Point(*list(map(lambda c: c[0] - c[1], zip(p1a, p1b))))
                    p2a, p2b = test.mapping[distance]
                    dp2 = Point(*list(map(lambda c: c[0] - c[1], zip(p2a, p2b))))
                    xform = list(map(lambda c: c[0] // c[1], zip(dp1, dp2)))

                    processed.append(process(inputs[j], permutation, xform))
                    good.append(processed[-1])
                    remaining.remove(j)
                    break

    return


def get_inputs():

    with Path("../inputs/19.txt").open("r") as handle:
        lines = list([line.strip() for line in handle.readlines()])

    lines = [
        "--- scanner 0 ---",
        "404,-588,-901",
        "528,-643,409",
        "-838,591,734",
        "390,-675,-793",
        "-537,-823,-458",
        "-485,-357,347",
        "-345,-311,381",
        "-661,-816,-575",
        "-876,649,763",
        "-618,-824,-621",
        "553,345,-567",
        "474,580,667",
        "-447,-329,318",
        "-584,868,-557",
        "544,-627,-890",
        "564,392,-477",
        "455,729,728",
        "-892,524,684",
        "-689,845,-530",
        "423,-701,434",
        "7,-33,-71",
        "630,319,-379",
        "443,580,662",
        "-789,900,-551",
        "459,-707,401",
        "",
        "--- scanner 1 ---",
        "686,422,578",
        "605,423,415",
        "515,917,-361",
        "-336,658,858",
        "95,138,22",
        "-476,619,847",
        "-340,-569,-846",
        "567,-361,727",
        "-460,603,-452",
        "669,-402,600",
        "729,430,532",
        "-500,-761,534",
        "-322,571,750",
        "-466,-666,-811",
        "-429,-592,574",
        "-355,545,-477",
        "703,-491,-529",
        "-328,-685,520",
        "413,935,-424",
        "-391,539,-444",
        "586,-435,557",
        "-364,-763,-893",
        "807,-499,-711",
        "755,-354,-619",
        "553,889,-390",
        "",
        "--- scanner 2 ---",
        "649,640,665",
        "682,-795,504",
        "-784,533,-524",
        "-644,584,-595",
        "-588,-843,648",
        "-30,6,44",
        "-674,560,763",
        "500,723,-460",
        "609,671,-379",
        "-555,-800,653",
        "-675,-892,-343",
        "697,-426,-610",
        "578,704,681",
        "493,664,-388",
        "-671,-858,530",
        "-667,343,800",
        "571,-461,-707",
        "-138,-166,112",
        "-889,563,-600",
        "646,-828,498",
        "640,759,510",
        "-630,509,768",
        "-681,-892,-333",
        "673,-379,-804",
        "-742,-814,-386",
        "577,-820,562",
        "",
        "--- scanner 3 ---",
        "-589,542,597",
        "605,-692,669",
        "-500,565,-823",
        "-660,373,557",
        "-458,-679,-417",
        "-488,449,543",
        "-626,468,-788",
        "338,-750,-386",
        "528,-832,-391",
        "562,-778,733",
        "-938,-730,414",
        "543,643,-506",
        "-524,371,-870",
        "407,773,750",
        "-104,29,83",
        "378,-903,-323",
        "-778,-728,485",
        "426,699,580",
        "-438,-605,-362",
        "-469,-447,-387",
        "509,732,623",
        "647,635,-688",
        "-868,-804,481",
        "614,-800,639",
        "595,780,-596",
        "",
        "--- scanner 4 ---",
        "727,592,562",
        "-293,-554,779",
        "441,611,-461",
        "-714,465,-776",
        "-743,427,-804",
        "-660,-479,-426",
        "832,-632,460",
        "927,-485,-438",
        "408,393,-506",
        "466,436,-512",
        "110,16,151",
        "-258,-428,682",
        "-393,719,612",
        "-211,-452,876",
        "808,-476,-593",
        "-575,615,604",
        "-485,667,467",
        "-680,325,-822",
        "-627,-443,-432",
        "872,-547,-609",
        "833,512,582",
        "807,604,487",
        "839,-516,451",
        "891,-625,532",
        "-652,-548,-490",
        "30,-46,-14",
        ]

    inputs = []

    for line in lines:
        if line.startswith("---"):
            readings = []
            continue
        if len(line) > 0:
            readings.append(Point(*list(map(int, line.split(",")))))
            continue
        inputs.append(readings)
        readings = []

    inputs.append(readings)

    return inputs


def process(points, permutation, mirroring):

    distances = []
    mapping = {}
    for p, point in enumerate(points):
        point = [point[permutation[0]], point[permutation[1]], point[permutation[2]]]
        for c in range(3):
            point[c] *= mirroring[c]
        points[p] = Point(*point)
    points = sorted(points)
    for i in range(len(points)-1):
        pti = points[i]
        for j in range(i+1, len(points)):
            ptj = points[j]
            distance = manhattan_distance(pti, ptj)
            distances.append(distance)
            mapping[distance] = (pti, ptj)

    return Info(points, set(distances), mapping)


def manhattan_distance(point_a, point_b):

    return tuple([abs(i-j) for i, j in zip(point_a, point_b)])


# results = defaultdict(list)
# good = [0]
# remaining = set(range(1, len(distances)))
# while len(good) > 0:
#     i = good.pop(0)
#     for j in list(remaining):
#         for permutation in permutations:
#             compare = set([(dist[permutation[0]], dist[permutation[1]], dist[permutation[2]]) for dist in distances[j].abs])
#             shared = list(distances[i].abs & compare)
#             if len(shared) == 66:
#
#                 d = shared[0]
#                 indices = distances[i].mapping[d][0]
#                 p1a, p1b = inputs[i][indices[0]], inputs[i][indices[1]]
#                 dp1 = Point(*list(map(lambda c: c[0] - c[1], zip(p1a, p1b))))
#                 indices = distances[j].mapping[d][0]
#                 p2a, p2b = inputs[j][indices[0]], inputs[j][indices[1]]
#                 dp2 = Point(*list(map(lambda c: c[0] - c[1], zip(p2a, p2b))))
#                 xform = Point(*list(map(lambda c: c[0] // c[1], zip(dp1, dp2))))
#
#                 results[i].append((j, permutation, xform))
#                 good.append(j)
#                 remaining.remove(j)
#                 break

if __name__ == "__main__":
    main()

