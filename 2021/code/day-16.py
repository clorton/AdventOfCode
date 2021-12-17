#! /usr/bin/env python3

from collections import Counter, defaultdict, namedtuple
from datetime import datetime
from functools import reduce
from heapq import heappush, heappop
from pathlib import Path

import numpy as np

t_start = datetime.now()

with Path("../inputs/16.txt").open("r") as handle:
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

bits = "".join(map(lambda i: f"{i:04b}", map(lambda h: int(h, 16), list(lines[0]))))


def literal(bits):

    more = int(bits[0])
    value = int(bits[1:5], 2)

    return value, more


version_sum = 0


def decode(bits):

    version = int(bits[0:3], 2)
    ptype = int(bits[3:6], 2)

    global version_sum
    version_sum += version

    if ptype == 4:
        count = 6
        data = 0
        while True:
            value, more = literal(bits[count:])
            count += 5
            data *= 16
            data += value
            if not more:
                break
        packet = (version, ptype, data)
    else:   # operator
        mode = int(bits[6:7])
        if mode == 0:
            length = int(bits[7:22], 2)
            subpackets = []
            consumed = 0
            while consumed < length:
                subpacket, count = decode(bits[22+consumed:])
                subpackets.append(subpacket)
                consumed += count
            packet = (version, ptype, subpackets)
            count = 22 + length
        else:   # mode == 1
            number = int(bits[7:18], 2)
            subpackets = []
            consumed = 0
            for p in range(number):
                subpacket, count = decode(bits[18+consumed:])
                subpackets.append(subpacket)
                consumed += count
            packet = (version, ptype, subpackets)
            count = 18 + consumed

    return packet, count


packet, count = decode(bits)
print(f"{version_sum=}")


def evaluate(packet):

    ptype = packet[1]
    payload = packet[2]
    if ptype == 0:
        assert len(payload) > 0
        return sum(map(evaluate, payload))
    elif ptype == 1:
        assert len(payload) > 0
        return reduce(lambda x, y: x*y, map(evaluate, payload), 1)
    elif ptype == 2:
        assert len(payload) > 0
        return min(map(evaluate, payload))
    elif ptype == 3:
        assert len(payload) > 0
        return max(map(evaluate, payload))
    elif ptype == 4:
        return payload
    elif ptype == 5:
        assert len(payload) == 2
        a = evaluate(payload[0])
        b = evaluate(payload[1])
        return 1 if a > b else 0
    elif ptype == 6:
        assert len(payload) == 2
        a = evaluate(payload[0])
        b = evaluate(payload[1])
        return 1 if a < b else 0
    elif ptype == 7:
        assert len(payload) == 2
        a = evaluate(payload[0])
        b = evaluate(payload[1])
        return 1 if a == b else 0
    else:
        raise RuntimeError


expression = evaluate(packet)
print(f"{expression=}")

t_finish = datetime.now()
print(f"Elapsed = {t_finish-t_start}")

pass
