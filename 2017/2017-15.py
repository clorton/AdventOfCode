#!/usr/bin/python


class Generator(object):
    def __init__(self, seed, factor):
        self._state = seed
        self._factor = factor
        pass

    def next(self):
        self._state = (self._state * self._factor) % 2147483647

        return self._state


class Generator2(object):
    def __init__(self, seed, factor, multiple):
        self._state = seed
        self._factor = factor
        self._multiple = multiple
        self._mask = multiple - 1
        pass

    def next(self):
        while True:
            self._state = (self._state * self._factor) % 2147483647
            if (self._state & self._mask) == 0:
                break

        return self._state


def main():

    # # generator_a = Generator(65, 16807)
    # # generator_b = Generator(8921, 48271)
    # generator_a = Generator(722, 16807)
    # generator_b = Generator(354, 48271)
    #
    # count = 0
    # for i in range(40000000):
    #     a = generator_a.next()
    #     b = generator_b.next()
    #     if (a & 0xFFFF) == (b & 0xFFFF):
    #         count += 1
    #
    # print('Count = {0}'.format(count))

    generator_a = Generator2(722, 16807, 4)
    generator_b = Generator2(354, 48271, 8)

    count = 0
    for i in range(5000000):
        a = generator_a.next()
        b = generator_b.next()
        if (a & 0xFFFF) == (b & 0xFFFF):
            count += 1

    print('Count = {0}'.format(count))

    return


def get_input(filename='2017-15.txt'):

    """
    Generator A starts with 722
    Generator B starts with 354
    """

    return None


if __name__ == '__main__':
    main()
