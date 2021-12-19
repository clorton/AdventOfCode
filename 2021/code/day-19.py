#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from pathlib import Path

import numpy as np

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

Point = namedtuple("Point", ["x", "y", "z"])

inputs = []

for line in lines:
    if line.startswith("---"):
        readings = []
        continue
    if len(line) > 0:
        readings.append(Point(*list(map(int, line.split(",")))))
        continue
    inputs.append(sorted(readings))
    readings = []

inputs.append(readings)

# scanners = [
#     [[0, 2], [4, 1], [3, 3]],
#     [[-1, -1], [-5, 0], [-2, 1]]
# ]


def manhattan_distance(point_a, point_b):

    return tuple([abs(i-j) for i, j in zip(point_a, point_b)])


Info = namedtuple("Info", ["abs", "mapping"])


def get_distances(scans):
    d = []
    for scanner in scans:
        dist = []
        mapping = defaultdict(list)
        for i in range(len(scanner)-1):
            for j in range(i+1, len(scanner)):
                distance = manhattan_distance(scanner[i], scanner[j])
                dist.append(distance)
                mapping[distance].append((i, j))
        d.append(Info(set(dist), mapping))

    return d


distances = get_distances(inputs)

permutations = [
    [0, 1, 2],
    [0, 2, 1],
    [1, 0, 2],
    [1, 2, 0],
    [2, 0, 1],
    [2, 1, 0]
]

results = defaultdict(list)
good = [0]
remaining = set(range(1, len(distances)))
while len(good) > 0:
    i = good.pop(0)
    for j in list(remaining):
        for permutation in permutations:
            compare = set([(dist[permutation[0]], dist[permutation[1]], dist[permutation[2]]) for dist in distances[j].abs])
            shared = list(distances[i].abs & compare)
            if len(shared) == 66:

                # p11 = distances[i][1][shared[0]][0][0]
                # p12 = distances[i][1][shared[0]][0][1]
                # p21 = distances[j][1][shared[0]][0][0]
                # p22 = distances[j][1][shared[0]][0][1]

                results[i].append((j, permutation))
                good.append(j)
                remaining.remove(j)
                break

alpha = 0   # 8
beta = 1    # 24
share = list(distances[alpha].abs & distances[beta].abs)

transforms = []
for d in share:
    _ = distances[alpha].mapping[d][0]
    p11 = inputs[alpha][_[0]]
    p12 = inputs[alpha][_[1]]
    dp1 = Point(p11.x - p12.x, p11.y - p12.y, p11.z - p12.z)
    _ = distances[beta].mapping[d][0]
    p21 = inputs[beta][_[0]]
    p22 = inputs[beta][_[1]]
    dp2 = Point(p21.x - p22.x, p21.y - p22.y, p21.z - p22.z)

    transform = Point(dp2.x // dp1.x, dp2.y // dp1.y, dp2.z // dp1.z)
    transforms.append(transform)

pass
