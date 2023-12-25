"""
https://adventofcode.com/2023/day/10
"""
from typing import List
from typing import Tuple
from typing import Set
from itertools import product
from collections import Counter
import pytest


def find_start(lines, nrows, ncols) -> List[Tuple[int, int, str]]:
    positions = product(range(nrows), range(ncols))
    irow0, icol0 = [(irow, icol) for irow, icol in positions if lines[irow][icol] == "S"][0]
    symbol = guess_first_symbol(lines, irow0, icol0, nrows, ncols)
    trail = [(irow0, icol0, symbol), ]
    return trail


def is_contained(trail, point):
    trail: List[Tuple[int, int, str]]
    point: Tuple[int, int]

    if point in [(r, c) for r, c, _ in trail]:
        return False

    irow0, icol0 = point

    # collect symbol data
    symbols = {
        "n": [(irow, icol, symbol) for irow, icol, symbol in trail[1:] if irow <= irow0 and icol == icol0 and symbol != "|"],
        "e": [(irow, icol, symbol) for irow, icol, symbol in trail[1:] if irow == irow0 and icol >= icol0 and symbol != "-"],
        "s": [(irow, icol, symbol) for irow, icol, symbol in trail[1:] if irow >= irow0 and icol == icol0 and symbol != "|"],
        "w": [(irow, icol, symbol) for irow, icol, symbol in trail[1:] if irow == irow0 and icol <= icol0 and symbol != "-"],
    }

    # sort symbols top to bottom and left to right
    symbols = {
        d: sorted(symbols[d], key=lambda elem: (elem[0], elem[1])) for d in ["n", "e", "s", "w"]
    }

    # stringify
    symbols = {
        d: "".join([elem[2] for elem in symbols[d]]) for d in ["n", "e", "s", "w"]
    }

    # count plain crossings
    crossings = Counter({
        "n": symbols["n"].count("-"),
        "e": symbols["e"].count("|"),
        "s": symbols["s"].count("-"),
        "w": symbols["w"].count("|"),
    })

    # remove plain symbols from data -- they have been accounted for
    symbols = {
        "n": symbols["n"].replace("-", ""),
        "e": symbols["e"].replace("|", ""),
        "s": symbols["s"].replace("-", ""),
        "w": symbols["w"].replace("|", ""),
    }

    # make pairs
    pairs = {
        d: [f"{a}{b}" for a, b in zip(symbols[d][::2], symbols[d][1::2])] for d in ["n", "e", "s", "w"]
    }

    patterns = {"FJ", "JF", "L7", "7L"}

    # remove pairs that aren't crossings given the direction
    pairs = {
        "n": ["-" if pair in patterns else pair for pair in pairs["n"]],
        "e": ["|" if pair in patterns else pair for pair in pairs["e"]],
        "s": ["-" if pair in patterns else pair for pair in pairs["s"]],
        "w": ["|" if pair in patterns else pair for pair in pairs["w"]],
    }

    crossings.update({
        "n": pairs["n"].count("-"),
        "e": pairs["e"].count("|"),
        "s": pairs["s"].count("-"),
        "w": pairs["w"].count("|")
    })

    return False not in [c % 2 == 1 for c in crossings.values()]


def get_data():
    ret = []
    testdata = [
        ("example1.txt", 1),
        ("example2.txt", 1),
        ("example3.txt", 4),
        ("example4.txt", 4),
        ("example5.txt", 8),
        ("example6.txt", 10),
        ("input.txt", 273)
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_dims(lines):
    return len(lines), len(lines[0])


def get_viable_connections(irow: int, icol: int, nrows: int, ncols: int, symbol: str) -> List[Tuple[int, int, Set[str]]]:
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


def guess_first_symbol(lines, irow0, icol0, nrows, ncols):
    for symbol in ["F", "-", "7", "|", "J", "L"]:
        conns = get_viable_connections(irow0, icol0, nrows, ncols, symbol)
        selected = [(irow, icol) for irow, icol, viable in conns if lines[irow][icol] in viable]
        if len(selected) == 2:
            return symbol
    raise "Shouldnt happen"


def move(trail, lines, nrows, ncols):
    trail: List[Tuple[int, int, str]]
    lines: List[List[str]]
    selected: List[Tuple[int, int, str]]

    irow, icol, _ = trail[-1]
    my_symbol = lines[irow][icol]
    conns = get_viable_connections(irow, icol, nrows, ncols, my_symbol)
    selected = []
    for irow, icol, viable in conns:
        if lines[irow][icol] in viable:
            selected.append((irow, icol, lines[irow][icol]))
    prev = trail[-2] if len(trail) >= 2 else None
    trail.append(selected[1] if selected[0] == prev else selected[0])
    return trail


def solve(txt):
    lines = txt.splitlines()
    nrows, ncols = get_dims(lines)
    trail = find_start(lines, nrows, ncols)
    lines = update_start_symbol(lines, trail)
    while True:
        trail = move(trail, lines, nrows, ncols)
        if trail[0] == trail[-1]:
            break
    positions = product(range(nrows), range(ncols))
    return [is_contained(trail, p) for p in positions].count(True)


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected


def update_start_symbol(lines, trail):
    irow0, icol0, symbol = trail[0]
    lines[irow0] = lines[irow0][:icol0] + symbol + lines[irow0][icol0 + 1:]
    return lines


def visualize(lines, trail):
    d = {
        "-": "\u2501",
        "|": "\u2503",
        "L": "\u2517",
        "J": "\u251B",
        "7": "\u2513",
        "F": "\u250F",
        ".": ".",
    }
    nrows, ncols = get_dims(lines)
    ndigits = len(str(ncols))
    for idigit in range(ndigits):
        print(f"{' ': >{ndigits}s} " + "".join([f"{icol: >{ndigits}d}"[idigit] for icol in range(ncols)]))
    for irow, line in enumerate(lines):
        arr = list(line)
        for icol in range(ncols):
            if (irow, icol, arr[icol]) in trail:
                arr[icol] = d[arr[icol]]
            elif is_contained(trail, (irow, icol)):
                arr[icol] = "o"
            else:
                arr[icol] = "."
        ncontained = arr.count("o")
        nout = "".join(arr).strip(".").count(".")
        print(f"{irow:>{ndigits}d} " + "".join(arr) + f" {ncontained: >{ndigits}d} / {nout: >{ndigits}d}")
