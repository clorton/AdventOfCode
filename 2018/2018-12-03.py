#!/usr/bin/python

from __future__ import print_function


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
        claim_id = elements[0]
        claims[claim_id] = [(elements[1], elements[2]), (elements[3], elements[4])]

    fabric = [[0 for _ in range(1000)] for __ in range(1000)]
    count = 0
    for claim_id in claims:
        claim = claims[claim_id]
        x_start = claim[0][0]
        y_start = claim[0][1]
        for y in range(claim[1][1]):
            for x in range(claim[1][0]):
                fabric[y_start+y][x_start+x] += 1
                if fabric[y_start+y][x_start+x] == 2:
                    count += 1

    print('Count = {0}'.format(count))

    return


def part2(lines):

    claims = {}
    for line in lines:
        elements = [int(entry) for entry in line.replace('#', '').replace('@', '').replace(',', ' ').replace(':', '').replace('x', ' ').split()]
        claim_id = elements[0]
        claims[claim_id] = [(elements[1], elements[2]), (elements[3], elements[4])]

    overlaps = {claim_id: False for claim_id in claims}
    for id_a in claims:
        if not overlaps[id_a]:
            for id_b in claims:
                if id_b != id_a:
                    a_xstart = claims[id_a][0][0]
                    b_xstart = claims[id_b][0][0]
                    a_xend = a_xstart + claims[id_a][1][0]
                    b_xend = b_xstart + claims[id_b][1][0]
                    a_ystart = claims[id_a][0][1]
                    b_ystart = claims[id_b][0][1]
                    a_yend = a_ystart + claims[id_a][1][1]
                    b_yend = b_ystart + claims[id_b][1][1]
                    if (a_xstart > b_xend) or (a_xend < b_xstart) or (a_ystart > b_yend) or (a_yend < b_ystart):
                        pass
                    else:
                        # print('{0} overlaps {1}'.format(claims[id_a], claims[id_b]))
                        overlaps[id_a] = True
                        continue

    for claim_id in overlaps:
        if not overlaps[claim_id]:
            print('Claim {0} does not overlap.'.format(claim_id))




    return


if __name__ == '__main__':
    main()
