#!/usr/bin/python

from __future__ import print_function
from collections import namedtuple


Claim = namedtuple('Claim', ['id', 'x', 'y', 'width', 'height'])


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-03.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


def part1(lines):

    claims = {}
    for line in lines:
        elements = [int(entry) for entry in line.replace('#', '').replace('@', '').replace(',', ' ').replace(':', '').replace('x', ' ').split()]
        claim = Claim(*elements)
        claims[claim.id] = claim

    fabric = [[0 for _ in range(1000)] for __ in range(1000)]
    count = 0
    for claim in claims.itervalues():
        for h in range(claim.height):
            for w in range(claim.width):
                fabric[claim.y+h][claim.x+w] += 1
                if fabric[claim.y+h][claim.x+w] == 2:
                    count += 1

    print('Count = {0}'.format(count))

    return


def part2(lines):

    claims = {}
    for line in lines:
        elements = [int(entry) for entry in line.replace('#', '').replace('@', '').replace(',', ' ').replace(':', '').replace('x', ' ').split()]
        claim = Claim(*elements)
        claims[claim.id] = claim

    overlaps = {claim_id: False for claim_id in claims}
    for id_a in claims:
        if not overlaps[id_a]:
            claim_a = claims[id_a]
            for id_b in claims:
                if id_b != id_a:
                    claim_b = claims[id_b]
                    if (claim_a.x > (claim_b.x + claim_b.width)) or ((claim_a.x + claim_a.width) < claim_b.x) or \
                            (claim_a.y > (claim_b.y + claim_b.height)) or ((claim_a.y + claim_a.height) < claim_b.y):
                        pass
                    else:
                        overlaps[id_a] = True
                        continue

    for claim_id in overlaps:
        if not overlaps[claim_id]:
            print('Claim {0} does not overlap.'.format(claim_id))

    return


if __name__ == '__main__':
    main()
