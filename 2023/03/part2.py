"""
https://adventofcode.com/2023/day/3
"""
import os
from pathlib import Path
import pytest


numerals = {str(i) for i in range(0, 10)}


def get_data():
    txt = "".join([
        "467..114..\n",
        "...*......\n",
        "..35..633.\n",
        "......#...\n",
        "617*......\n",
        ".....+.58.\n",
        "..592.....\n",
        "......755.\n",
        "...$.*....\n",
        ".664.598..\n",
    ])
    expected = sum([467 * 35, 755 * 598])
    return [
        pytest.param((txt, expected), id="example")
    ]


def main():
    d = os.path.dirname(os.path.realpath(__file__))
    f = Path(d, "input.txt")
    with open(f, "rt") as fid:
        txt = fid.read()
    print(solve(txt))


def get_positions_neighboring_numerals(data, irow, icol, nrows, ncols):
    can_north = irow >= 1
    can_east = icol <= ncols - 2
    can_south = irow <= nrows - 2
    can_west = icol >= 1

    northwest = (irow - 1, icol - 1) if can_north and can_west else None
    north = (irow - 1, icol) if can_north else None
    northeast = (irow - 1, icol + 1) if can_north and can_east else None
    west = (irow, icol - 1) if can_west else None
    east = (irow, icol + 1) if can_east else None
    southwest = (irow + 1, icol - 1) if can_south and can_west else None
    south = (irow + 1, icol) if can_south else None
    southeast = (irow + 1, icol + 1) if can_south and can_east else None

    directions = [d for d in [northwest, north, northeast, west, east, southwest, south, southeast] if d is not None]
    return [(irow, icol) for irow, icol in directions if data[irow][icol] in numerals]


def find_part_numbers(data, neighbor_positions):
    part_ids = []
    starts = []
    for irow, icol in neighbor_positions:
        # walk left to find the start of the part number
        while icol >= 1 and data[irow][icol - 1] in numerals:
            icol = icol - 1
        starts.append((irow, icol))
    # unique list of starting points
    ustarts = sorted(set(starts))
    if len(ustarts) <= 1:
        # not a gear, need to be touching exactly two part numbers
        return 0, 0
    elif len(ustarts) == 2:
        # valid gear symbol
        ncols = len(data[0])
        for irow, icol in ustarts:
            icol_start = icol
            # walk right to find the end of the part number
            while icol <= ncols - 2 and data[irow][icol + 1] in numerals:
                icol = icol + 1
            icol_end = icol
            part_id = int("".join(data[irow][icol_start:icol_end + 1]))
            part_ids.append(part_id)
        return *part_ids,
    else:
        print("didnt expect this to happen")


def prep_data(txt):
    assert txt[-1] == "\n", "Expected last character to be a newline"
    data = [list(line) for line in txt.splitlines()]
    ncols = len(data[0])
    nrows = len(data)
    return nrows, ncols, data


def find_gear_symbol_positions(data):
    positions = []
    nrows = len(data)
    for irow in range(nrows):
        icol = 0
        ngears = data[irow].count("*")
        for _ in range(ngears):
            icol = data[irow].index("*", icol)
            positions.append((irow, icol))
            icol = icol + 1
    return positions


def solve(txt):
    nrows, ncols, data = prep_data(txt)
    gear_positions = find_gear_symbol_positions(data)
    ratios = []
    for irow, icol in gear_positions:
        neighbor_positions = get_positions_neighboring_numerals(data, irow, icol, nrows, ncols)
        part_id_1, part_id_2 = find_part_numbers(data, neighbor_positions)
        ratios.append(part_id_1 * part_id_2)
    return sum([r for r in ratios if r > 0])


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected


if __name__ == "__main__":
    main()
