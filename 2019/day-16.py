#!/usr/bin/env python3

import numpy as np

pattern = [0, 1, 0, -1]


def do_phase(_inputs, count, show=True, verbose=False):
    current = list(_inputs)
    for phase in range(count):
        subsequent = [0 for _ in range(len(_inputs))]
        for digit in range(len(_inputs)):
            total = 0
            if verbose:
                print()
                print(f"Calculating digit {digit}: ", end="")
            for source in range(len(_inputs)):
                lookup = (source + 1) // (digit + 1)
                a = current[source]
                b = pattern[lookup % len(pattern)]
                if verbose:
                    print(f"{a} * {b} + ", end="")
                total += a * b
            subsequent[digit] = abs(total) % 10
        current = subsequent
        if verbose:
            print()
        if show:
            last = ''.join([f'{_}' for _ in current])
            print(f"{phase}: {last}")

    return ''.join([f'{_}' for _ in current])


def part2(inputs, phases=100, verbose=False):

    offset = int(''.join([f"{inputs[index]}" for index in range(7)]))
    tenk = 10000 * len(inputs)

    data = np.zeros((phases+1, tenk-offset), dtype=np.uint8)
    for index in range(offset, tenk):
        data[0, index-offset] = inputs[index % len(inputs)]

    # print(f"{data[0, 0:8]}")
    for phase in range(phases):
        total = 0
        for index in range(tenk-1, offset-1, -1):
            total += data[phase, index-offset]
            total %= 10
            data[phase+1, index-offset] = total
        if verbose:
            print(f"{phase+1:03}: {data[phase+1, 0:8]}")

    return f"{data[phases, 0:8]}"


def main():

    inputs = "59765216634952147735419588186168416807782379738264316903583191841332176615408501571822799985693486107923593120590306960233536388988005024546603711148197317530759761108192873368036493650979511670847453153419517502952341650871529652340965572616173116797325184487863348469473923502602634441664981644497228824291038379070674902022830063886132391030654984448597653164862228739130676400263409084489497532639289817792086185750575438406913771907404006452592544814929272796192646846314361074786728172308710864379023028807580948201199540396460310280533771566824603456581043215999473424395046570134221182852363891114374810263887875638355730605895695123598637121"
    inputs = [int(digit) for digit in list(inputs)]

    # Test case 1
    do_phase([int(digit) for digit in list("12345678")], 4, show=True)  # , verbose=True)
    print()
    # Test cases 2, 3, 4
    print(do_phase([int(digit) for digit in list("80871224585914546619083218645595")], 100, False))
    print(do_phase([int(digit) for digit in list("19617804207202209144916044189917")], 100, False))
    print(do_phase([int(digit) for digit in list("69317163492948606335995924319873")], 100, False))
    # Actual input
    print(do_phase(inputs, 100, False))

    # Part 2

    # Test cases 1, 2, 3
    print(part2([int(digit) for digit in "03036732577212944063491565474664"]))
    print(part2([int(digit) for digit in "02935109699940807407585447034323"]))
    print(part2([int(digit) for digit in "03081770884921959731165446850517"]))
    # Actual input
    print(part2(inputs))

    return


if __name__ == "__main__":
    main()
