"""Solution for Advent of Code 2022 Day 20 Challenge"""

# from collections import namedtuple
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Union

import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / "2022-20.txt"


def get_inputs(filename:Path = INPUTFILE) -> List[Union[str,int]]:

    """Read inputs from given filename."""

    with filename.open("r") as file:
        inputs = [int(line.strip()) for line in file.readlines()]

    # test = [1,2,-3,3,-2,0,4]
    # inputs = test

    print(inputs[0:8])

    return inputs

VALUE = 0
NEXT = 1
PREV = 2


def make_list(inputs:List[int], key:int=1) -> np.ndarray:

    """Make linked list from given inputs. Optionally multiply values by 'decryption' key."""

    length = len(inputs)
    linked = np.zeros((length, 3), dtype=np.int64)

    for index, value in enumerate(inputs):
        linked[index, VALUE] = value*key
        linked[index, NEXT] = (index+1)%length
        linked[index, PREV] = (index-1)%length

    return linked


def unlink(index: int, linkedlist: np.ndarray) -> None:

    """Unlink an item from the linked list."""

    next_node = linkedlist[index, NEXT]
    prev_node = linkedlist[index, PREV]
    linkedlist[next_node, PREV] = prev_node
    linkedlist[prev_node, NEXT] = next_node
    # linkedlist[index, NEXT] = 666_666     # leave this "valid" as a "header"
    # linkedlist[index, PREV] = 666_666     # leave this "valid" as a "header"

    # return


def insert_after(target: int, index: int, linkedlist: np.ndarray) -> None:

    """Insert given item (index) after target node."""

    save_next = linkedlist[target, NEXT]
    linkedlist[index, NEXT] = save_next
    linkedlist[index, PREV] = target
    linkedlist[target, NEXT] = index
    linkedlist[save_next, PREV] = index

    # return


def insert_before(target: int, index: int, linkedlist: np.ndarray) -> None:

    """Insert given item (index) before target node."""

    save_prev = linkedlist[target, PREV]
    linkedlist[index, NEXT] = target
    linkedlist[index, PREV] = save_prev
    linkedlist[target, PREV] = index
    linkedlist[save_prev, NEXT] = index

    # return


def get_context(index:int, linked:np.ndarray) -> str:

    """Show values surrounding given node."""

    cminus = linked[index, PREV]
    cminusminus = linked[cminus, PREV]
    cplus = linked[index, NEXT]
    cplusplus = linked[cplus, NEXT]

    return f"{linked[cminusminus,VALUE]:5}...{linked[cminus,VALUE]:5}..>{linked[index,VALUE]:5}<..{linked[cplus,VALUE]:5}...{linked[cplusplus,VALUE]:5}"


def mix(inputs: List[int], linkedlist: np.ndarray, iteration: Union[int,str]="?") -> timedelta:

    """Mix the list of values according to the elfs' process."""

    tstart = datetime.now()

    length = len(inputs)

    for index, value in enumerate(inputs):

        if index < 8:
            print(f"Processing value {index} == {value:5}: ", end="")

        if value == 0:
            continue

        skip = value

        subsequent, previous = linkedlist[index,NEXT:]
        unlink(index, linkedlist)
        current = index

        if skip > 0:

            current = subsequent    # linkedlist[current, NEXT]
            skip -= 1

            skip = (skip % (length-1))

            for _ in range(skip):
                current = linkedlist[current, NEXT]

            if index < 8:
                print(f"inserting {index} after  {current:4} {get_context(current, linkedlist)}")

            insert_after(current, index, linkedlist)

        else:   # skip < 0:

            current = previous  # linkedlist[current, PREV]
            skip += 1

            skip = (abs(skip) % (length-1))

            for _ in range(abs(skip)):
                current = linkedlist[current, PREV]

            if index < 8:
                print(f"inserting {index} before {current:4} {get_context(current, linkedlist)}")

            insert_before(current, index, linkedlist)

    tend = datetime.now()

    if length <= 16:
        print(f"{iteration}: ", end="")
        current = 0
        for _ in range(length):
            print(f"{linkedlist[current, VALUE]} ", end="")
            current = linkedlist[current, NEXT]
        print()

    return tend-tstart


def get_coordinates(linkedlist, elapsed):

    """Get grove coordinates from 1000th, 2000th, and 3000th item after item with value 0 (zero)."""

    izero = np.nonzero(linkedlist[:,VALUE] == 0)[0][0]
    print(f"Item 0 found at index {izero}.")

    current = izero
    for _ in range(1000):
        current = linkedlist[current, NEXT]
    einsk = linkedlist[current, VALUE]
    for _ in range(1000):
        current = linkedlist[current, NEXT]
    zweik = linkedlist[current, VALUE]
    for _ in range(1000):
        current = linkedlist[current, NEXT]
    dreik = linkedlist[current, VALUE]

    print(f"{elapsed}: {einsk=}, {zweik=}, {dreik=} ... {einsk+zweik+dreik}")

    # return


def main(part1: bool, part2: bool) -> None:

    """Run none, one, or both parts of 2022 Day 20 challenge."""

    inputs = get_inputs()

    if part1:

        linked = make_list(inputs)
        elapsed = mix(inputs, linked)
        if len(inputs) == 5000:
            print("Part 1 actual answer: einsk=6439, zweik=853, dreik=7596 ... 14888")
        else:
            print("Part 1 test answer: einsk=4, zweik=-3, dreik=2 ... 3")
        get_coordinates(linked, elapsed)

    if part2:

        decrypted = make_list(inputs, key=811589153)

        if len(decrypted) <= 16:
            print(" ".join(map(str, decrypted[:,VALUE])))

        elapsed = timedelta()
        for _ in range(10):
            elapsed += mix(inputs, decrypted, _)

        if len(inputs) == 5000:
            print("Part 2 actual answer: einsk=???, zweik=???, dreik=??? ... ???")
        else:
            print("Part 2 test answer: einsk=811589153, zweik=2434767459, dreik=-1623178306 ... 1623178306")

        # 5449009573242 is too high...
        get_coordinates(decrypted, elapsed)

    # return


def unittest() -> None:

    """Do unittests (and more)..."""

    def move_forward(delta:int, linked:np.ndarray, start:int=1, display=False) -> None:

        """Simulate positive value mixing."""

        current = start
        for _ in range(delta%len(linked)):
            current = linked[current, NEXT]
        if current != start:
            unlink(start, linked)
            if display:
                print(f"*nserting {start} after  {current:4} {get_context(current, linked)}")
            insert_after(current, start, linked)

        # return

    def move_backward(delta:int, linked:np.ndarray, start:int=1, display=False) -> None:

        """Simulate positive value mixing."""

        current = start
        for _ in range(delta%len(linked)):
            current = linked[current, PREV]
        if current != start:
            unlink(start, linked)
            if display:
                print(f"*nserting {start} before {current:4} {get_context(current, linked)}")
            insert_before(current, start, linked)

        # return

    def print_list(linked:np.ndarray, mapping=chr) -> None:

        """Display list in current order."""

        current = 0
        while True:
            print(f"{mapping(linked[current, VALUE])} ", end="")
            current = linked[current, NEXT]
            if current == 0:
                break
        print()

        # return

    # inputs = [ord(c) for c in "ABCDE"]
    # linked = make_list(inputs)
    # print_list(linked)

    # for delta in range(0, 14):

    #     linked = make_list(inputs)
    #     print(f"Move 'B' {delta:2} nodes forward: ", end="")
    #     move_forward(delta, linked)
    #     print_list(linked)

    # print("\n-----=====#####=====-----\n")

    # for delta in range(0, 14):

    #     linked = make_list(inputs)
    #     print(f"Move 'B' {delta:2} nodes backward: ", end="")
    #     move_backward(delta, linked)
    #     print_list(linked)

    # print("\n-------------------------\n")

    def do_mix(deltas:List[int], linked:np.ndarray, debug:bool=False) -> None:

        _ = print_list(linked, mapping=int) if debug else None
        for index, delta in enumerate(deltas):
            if delta == 0:
                continue
            if index < 8:
                print(f"*rocessing value {index} = {delta:5}: ", end="")
            if delta > 0:
                move_forward(delta, linked, start=index, display=index<8)
            else:   # delta < 0
                move_backward(-delta, linked, start=index, display=index<8)
            _ = print_list(linked, mapping=int) if debug else None

        # return

    def get_coords(linked:np.ndarray) -> List[int]:

        izero = np.nonzero(linked[:,VALUE] == 0)[0][0]
        current = izero
        for _ in range(1000):
            current = linked[current, NEXT]
        eins = linked[current, VALUE]
        for _ in range(1000):
            current = linked[current, NEXT]
        zwei = linked[current, VALUE]
        for _ in range(1000):
            current = linked[current, NEXT]
        drei = linked[current, VALUE]

        return [eins, zwei, drei]

    # test = [ord(c) for c in "ABCDEFG"]
    # linked = make_list(test)
    # print_list(linked)
    # deltas = [1,2,-3,3,-2,0,4]
    # do_mix(deltas, linked)
    # print_list(linked)
    # print("Expected: [A, B, C, G, F, D, E]")

    # print("\n-------------------------\n")

    # linked = make_list(deltas)
    # do_mix(deltas, linked)
    # coords = get_coords(linked)
    # print(f"{coords=} => {sum(coords)}")

    # print("\n- Part 1 (test): --------\n")

    # deltas = [1,2,-3,3,-2,0,4]
    # linked = make_list(deltas)
    # do_mix(deltas, linked, debug=True)
    # coords = get_coords(linked)
    # print(f"{coords=} => {sum(coords)}")
    # print("Expect:[4, -3, 2] => 3")

    print("\n- Part 1: ---------------\n")

    inputs = get_inputs()
    linked = make_list(inputs)
    do_mix(inputs, linked)
    coords = get_coords(linked)
    print(f"{coords=} => {sum(coords)}")
    print("Expect:[6439, 853, 7596] => 14888")

    # print("\n- Part 2 (test): --------\n")

    # linked = make_list(deltas, key=811589153)
    # for _ in range(10):
    #     do_mix(deltas, linked)  # , debug=True)
    # coords = get_coords(linked)
    # print(f"{coords=} => {sum(coords)}")
    # print("Expect:[811589153, 2434767459, -1623178306] => 1623178306")

    # return


if __name__ == "__main__":
    unittest()
    main(True, False)
