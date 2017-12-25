#!/usr/bin/python

from collections import deque, namedtuple

Component = namedtuple('Component', ['a', 'b'])
Node = namedtuple('Node', ['a', 'b', 'children'])
Candidate = namedtuple('Candidate', ['node', 'available'])


def main():

    components = []
    with open('2017-24.txt', 'r') as handle:
        for line in handle.readlines():
            a, b = [item for item in map(int, line.split('/'))]
            components.append(Component(a, b))

    first = Node(0, 0, [])
    search = deque()
    search.append(Candidate(first, components[:]))
    while len(search) > 0:
        node, available = search.pop()
        for candidate in available:
            if node.b in candidate:
                child = Node(candidate.a, candidate.b, []) if candidate.a == node.b else Node(candidate.b, candidate.a, [])
                node.children.append(child)
                remaining = available[:]
                remaining.remove(candidate)
                search.append(Candidate(child, remaining))

    strongest = strongest_path(first)
    print('Strongest bridge is {0}'.format(strongest))

    longest, strongest = longest_path(first)
    print('Longest bridge is {0} components and {1} strong'.format(longest, strongest))

    return


def strongest_path(node):
    best = 0
    for child in node.children:
        strength = strongest_path(child)
        if strength > best:
            best = strength

    return best + (node.a + node.b)


def longest_path(node, size=0):
    longest = size
    strongest = 0
    for child in node.children:
        length, strength = longest_path(child, size+1)
        if (length > longest) or ((length == longest) and (strength > strongest)):
            longest = length
            strongest = strength

    return longest, strongest + (node.a + node.b)


if __name__ == '__main__':
    main()
