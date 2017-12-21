#!/usr/bin/python

from collections import defaultdict, deque
from math import sqrt
import re
import sys


class Vector(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        return

    def __add__(self, other):

        return Vector(self.a + other.a, self.b + other.b, self.c + other.c)

    def __eq__(self, other):

        return (self.a == other.a) and (self.b == other.b) and (self.c == other.c)

    def __hash__(self):

        return hash((self.a, self.b, self.c))

    @property
    def magnitude(self):

        return sqrt(self.a * self.a + self.b * self.b + self.c * self.c)

    def __str__(self):

        return '({0},{1},{2})'.format(self.a, self.b, self.c)


class Particle(object):
    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

        return

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity

        return

    @property
    def distance(self):

        return self.position.magnitude

    def __str__(self):

        return '{0},{1},{2}'.format(self.position, self.velocity, self.acceleration)


def main():

    data = get_input()
    particles = parse_data(data)

    for i in range(1000):
        for particle in particles:
            particle.update()

    distances = [particle.distance for particle in particles]

    index = -1
    minimum = sys.float_info.max
    for i in range(len(distances)):
        if distances[i] < minimum:
            index = i
            minimum = distances[i]

    print('Minimum particle distance particle {0} ({1})'.format(index, minimum))

    particles = parse_data(data)

    for i in range(100):
        positions = defaultdict(deque)
        for p in range(len(particles)):
            positions[particles[p].position].append(p)

        for position, entries in positions.items():
            if len(entries) > 1:
                print('Particles {0} collided at i = {1}'.format(entries, i))
                while len(entries) > 0:
                    del particles[entries.pop()]

        for particle in particles:
            particle.update()

    print('{0} particles remaining'.format(len(particles)))

    particles = parse_data(data)

    collided = set()
    for i in range(len(particles)):
        for j in range(i, len(particles)):
            t = intersect(particles[i], particles[j])
            if t:
                collided.add(i)
                collided.add(j)
                print('Particle {0}, ({1}), intersects particle {2}, ({3}), at time {4}'.format(i, particles[i], j, particles[j], t))

    print('{0} particles collide'.format(len(collided)))
    print('{0} particles remaining'.format(len(particles)-len(collided)))

    return


def parse_data(data):

    pattern = re.compile('[pva]=<([-0-9]+),([-0-9]+),([-0-9]+)>')
    particles = []
    for entry in data:
        parts = entry.split(', ')
        p_a, p_b, p_c = [int(g) for g in pattern.match(parts[0]).groups()]
        v_a, v_b, v_c = [int(g) for g in pattern.match(parts[1]).groups()]
        a_a, a_b, a_c = [int(g) for g in pattern.match(parts[2]).groups()]
        particle = Particle(Vector(p_a, p_b, p_c), Vector(v_a, v_b, v_c), Vector(a_a, a_b, a_c))
        particles.append(particle)

    return particles


def intersect(a, b):

    def time(pa0, va0, aa0, pb0, vb0, ab0):
        A = (aa0 - ab0) / 2
        B = (va0 - vb0) + A
        C = (pa0 - pb0)
        if A != 0:  # quadratic
            root = B * B - 4 * A * C
            if (root >= 0) and (sqrt(root) == int(sqrt(root))) and (A != 0):
                t = (-B + sqrt(root)) / (2 * A)
                if t == int(t):
                    return t
                t = (-B - sqrt(root)) / (2 * A)
                if t == int(t):
                    return t
        elif B != 0:   # linear
            t = -C / B
            if t == int(t):
                return t
        elif C == 0:
            return 0

        return None

    tx = time(a.position.a, a.velocity.a, a.acceleration.a, b.position.a, b.velocity.a, b.acceleration.a)
    ty = time(a.position.b, a.velocity.b, a.acceleration.b, b.position.b, b.velocity.b, b.acceleration.b)
    tz = time(a.position.c, a.velocity.c, a.acceleration.c, b.position.c, b.velocity.c, b.acceleration.c)
    if tx and (tx == ty) and (tx == tz):
        return tx

    return None


def get_input(filename='2017-20.txt'):

    with open(filename, 'r') as handle:
        data = handle.readlines()

    return data


if __name__ == '__main__':
    main()
