"""
https://adventofcode.com/2023/day/10
"""
from typing import List
from typing import Tuple
from itertools import product
import pytest


def find_start(lines, nrows, ncols) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    positions = product(range(nrows), range(ncols))
    trail = [(irow, icol) for irow, icol in positions if lines[irow][icol] == "S"]
    symbol = guess_first_symbol(trail, lines, nrows, ncols)
    irow0, icol0 = trail[0]
    lines[irow0] = lines[irow0][:icol0] + symbol + lines[irow0][icol0 + 1:]
    return trail, lines


def get_data():
    ret = []
    testdata = [
        ("example1.txt", 4),
        ("example2.txt", 8),
        ("input.txt", 6947)
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_dims(lines):
    return len(lines), len(lines[0])


def get_viable_connections(irow, icol, nrows, ncols, symbol):
    d = {
        "F": [
            {},
            {"-", "J", "7"},
            {"|", "J", "L"},
            {},
        ],
        "-": [
            {},
            {"7", "-", "J"},
            {},
            {"F", "-", "L"},
        ],
        "7": [
            {},
            {},
            {"|", "J", "L"},
            {"F", "-", "L"},
        ],
        "|": [
            {"F", "7", "|"},
            {},
            {"|", "J", "L"},
            {},
        ],
        "J": [
            {"F", "7", "|"},
            {},
            {},
            {"F", "-", "L"},
        ],
        "L": [
            {"F", "7", "|"},
            {"-", "J", "7"},
            {},
            {},
        ],
        ".": [
            {},
            {},
            {},
            {},
        ],
    }
    positions = [
        (irow - 1, icol),
        (irow, icol + 1),
        (irow + 1, icol),
        (irow, icol - 1),
    ]
    return [(r, c, viable) for (r, c), viable in zip(positions, d[symbol]) if 0 <= r <= nrows - 1 and 0 <= c <= ncols - 1]


def guess_first_symbol(trail, lines, nrows, ncols):
    irow0, icol0 = trail[0]
    for symbol in ["F", "-", "7", "|", "J", "L"]:
        conns = get_viable_connections(irow0, icol0, nrows, ncols, symbol)
        selected = [(irow, icol) for irow, icol, viable in conns if lines[irow][icol] in viable]
        if len(selected) == 2:
            return symbol
    raise "Shouldnt happen"


def move(trail, lines, nrows, ncols):
    irow, icol = trail[-1]
    my_symbol = lines[irow][icol] if lines[irow][icol] != "S" else guess_first_symbol(trail, lines, nrows, ncols)
    conns = get_viable_connections(irow, icol, nrows, ncols, my_symbol)
    selected = [(irow, icol) for irow, icol, viable in conns if lines[irow][icol] in viable]
    prev = (-1, -1) if len(trail) == 1 else trail[-2]
    trail.append(selected[0] if selected[0] != prev else selected[1])
    return trail


def solve(txt):
    lines = txt.splitlines()
    nrows, ncols = get_dims(lines)
    trail, lines = find_start(lines, nrows, ncols)
    while True:
        trail = move(trail, lines, nrows, ncols)
        if trail[0] == trail[-1]:
            break
    return (len(trail) - 1) / 2


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
