#! /usr/bin/env python3

from collections import Counter, defaultdict, namedtuple
from datetime import datetime
from functools import reduce
from heapq import heappush, heappop
from pathlib import Path

import numpy as np

t_start = datetime.now()

with Path("../inputs/17.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

"""
lines = [
    # "D2FE28"
    # "38006F45291200"
    # "EE00D40C823060"
    # "8A004A801A8002F478"              # version sum = 16
    # "620080001611562C8802118E34"      # version sum = 12
    # "C0015000016115A2E0802F182340"    # version sum = 23
    # "A0016C880162017C3686B18A3D4780"  # version sum = 31
    "C200B40A82"                    # 1 + 2 = 3
    "04005AC33890"                  # 6 * 9 = 54
    "880086C3E88112"                # min(7, 8, 9) = 7
    "CE00C43D881120"                # max(7, 8, 9) = 9
    "D8005AC2A8F0"                  # 5 < 15 = 1
    "F600BC2D8F"                    # 5 !< 15 = 0
    "9C005AC2F8F0"                  # 5 != 15 = 0
    "9C0141080250320F1802104A08"    # (1 + 3) == (2 * 2) = 1
]
"""

t_finish = datetime.now()
print(f"Elapsed = {t_finish-t_start}")

pass
