"""
https://adventofcode.com/2023/day/3
"""
import pytest


numerals = {str(i) for i in range(0, 10)}


def get_data():
    ret = []
    testdata = [
        ("example.txt", sum([467, 35, 633, 617, 592, 755, 664, 598])),
        ("input.txt", 556367),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_part_id(data, *, irow, icol):
    assert data[irow][icol] in numerals

    ncols = len(data[0])
    nrows = len(data)
    assert 0 <= irow <= nrows, "Row index out of bounds"
    assert 0 <= icol <= ncols, "Row index out of bounds"

    # walk left to find start of multi digit number
    while icol >= 1 and data[irow][icol - 1] in numerals:
        icol = icol - 1
    icol_start = icol
    # walk right to find end of multi digit number
    while icol <= ncols - 2 and data[irow][icol + 1] in numerals:
        icol = icol + 1
    icol_end = icol

    cutout = []
    inner = []
    for icol in range(icol_start, icol_end + 1):
        cutout = cutout + get_neighbors(irow, icol, nrows, ncols)
        inner.append((irow, icol))
    cutout = sorted(set(cutout) - set(inner))

    part_id = int("".join(data[irow][icol_start:icol_end + 1]))
    has_adjacent_symbol = len("".join([data[irow][icol].replace(".", "") for irow, icol in cutout])) > 0
    return part_id if has_adjacent_symbol else None, icol_end


def get_neighbors(irow, icol, nrows, ncols):
    can_north = irow >= 1
    can_east = icol <= ncols - 2
    can_south = irow <= nrows - 2
    can_west = icol >= 1

    northwest = (irow - 1, icol - 1) if can_north & can_west else None
    north = (irow - 1, icol) if can_north else None
    northeast = (irow - 1, icol + 1) if can_north & can_east else None
    west = (irow, icol - 1) if can_west else None
    east = (irow, icol + 1) if can_east else None
    southwest = (irow + 1, icol - 1) if can_south and can_west else None
    south = (irow + 1, icol) if can_south else None
    southeast = (irow + 1, icol + 1) if can_south & can_east else None

    directions = [northwest, north, northeast, west, east, southwest, south, southeast]
    return [d for d in directions if d is not None]


def prep_data(txt):
    assert txt[-1] == "\n", "Expected last character to be a newline"
    data = [list(line) for line in txt.splitlines()]
    ncols = len(data[0])
    nrows = len(data)
    return nrows, ncols, data


def solve(txt):
    nrows, ncols, data = prep_data(txt)
    part_ids = []
    for irow in range(nrows):
        icol = 0
        while icol <= ncols - 2:
            if data[irow][icol] in numerals:
                part_id, icol = get_part_id(data, irow=irow, icol=icol)
                if part_id is not None:
                    part_ids.append(part_id)
            icol = icol + 1
    return sum(part_ids)


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
