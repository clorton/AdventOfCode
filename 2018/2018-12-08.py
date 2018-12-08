#!/usr/bin/python

from __future__ import print_function


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-08.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


def part1(lines):

    data = [int(entry) for entry in lines[0].split()]
    data.reverse()

    tree, _ = parse(data)

    print('Sum of metadata is {0}'.format(metadata_sum))

    return


metadata_sum = 0


def parse(data):

    global metadata_sum
    child_count = data.pop()
    metadata_count = data.pop()
    entry = {'child_count': child_count, 'metadata_count': metadata_count, 'children': [], 'metadata': []}
    for i in range(child_count):
        child, data = parse(data)
        entry['children'].append(child)
    for i in range(metadata_count):
        metadata = data.pop()
        metadata_sum += metadata
        entry['metadata'].append(metadata)

    return entry, data


def part2(lines):

    data = [int(entry) for entry in lines[0].split()]
    data.reverse()

    tree, _ = parse(data)

    answer = valueof(tree)

    print('Value of root node is {0}'.format(answer))

    return


def valueof(node):

    if node['child_count'] == 0:
        value = sum(node['metadata'])
    else:
        value = 0
        for data in node['metadata']:
            if data == 0:
                pass
            else:
                data -= 1
                if data < node['child_count']:
                    value += valueof(node['children'][data])

    return value


if __name__ == '__main__':
    main()
