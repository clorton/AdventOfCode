#!/usr/bin/env python3

from collections import namedtuple
import re

from pathlib import Path
WORK_DIR = Path(__file__).parent.absolute()

with (WORK_DIR / "2017-07.txt").open("r") as handle:
    lines = handle.readlines()

Entry = namedtuple('Entry', ['weight', 'parent'])
Node = namedtuple('Node', ['weight', 'children'])


def set_weight(name, weight, library):
    library[name] = Entry(weight, library[name].parent) if name in library else Entry(weight, None)

    return


def set_parent(child, parent, library):
    library[child] = Entry(library[child].weight, parent) if child in library else Entry(None, parent)

    return


def calculate_weights(tree, root, weights):
    weight = tree[root].weight
    children = tree[root].children
    for child in children:
        calculate_weights(tree, child, weights)
        weight += weights[child].weight
    weights[root] = Node(weight, children)

    return


def find_imbalance(weights, root):

    oddball = None
    actual = 0
    expected = 0
    while root:
        map = {}
        children = weights[root].children
        for child in children:
            count = 0
            for sibling in children:
                if weights[sibling].weight == weights[child].weight:
                    count += 1
            map[count] = child
        if len(map) == 2:
            oddball = map[1]
            sibling = map[len(children)-1]
            actual = weights[oddball].weight
            expected = weights[sibling].weight
            print("'{0}' has weight {1}, siblings have weight {2}".format(oddball, actual, expected))
            root = oddball
        else:
            print("All of {0}'s children have the same weight.".format(root))
            root = None

    return oddball, actual, expected


def main():
    library = {}
    spec = re.compile('([a-z]+) \(([0-9]+)\)')
    for line in lines:
        parts = [part.strip() for part in line.split('->')]
        name, weight = spec.match(parts[0]).groups()
        # if len(parts) == 1:
        #     library[name] = Entry(weight, None)
        # else:
        #     children = [child.strip() for child in parts[1].split(',')]
        #     library[name] = Entry(weight, children)
        set_weight(name, int(weight), library)
        if len(parts) > 1:
            children = [child.strip() for child in parts[1].split(',')]
            for child in children:
                set_parent(child, name, library)

    for item in library:
        if library[item].weight is None:
            print("Weight of item '{0}' is None.".format(item))
        if library[item].parent is None:
            print("Parent of item '{0}' is None.".format(item))
            root = item

    tree = {}
    for line in lines:
        parts = [part.strip() for part in line.split('->')]
        name, weight = spec.match(parts[0]).groups()
        children = [child.strip() for child in parts[1].split(',')] if len(parts) > 1 else []
        tree[name] = Node(int(weight), children)

    weights = {}
    calculate_weights(tree, root, weights)
    oddball, actual, expected = find_imbalance(weights, root)
    correct = library[oddball].weight
    correct += expected - actual
    print('Oddball program is {0}, actual weight is {1}, should be {2}.'.format(oddball, library[oddball].weight, correct))

    return


if __name__ == '__main__':
    main()
