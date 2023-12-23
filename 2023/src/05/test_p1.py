"""
https://adventofcode.com/2023/day/5
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", min([82, 43, 86, 35])),
        ("input.txt", 261668924),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_seed_ids(lines):
    return [int(elem) for elem in lines[0].split(":", maxsplit=1)[1].strip().split()]


def apply_table(table, i):
    for (tgt, src, rng) in table:
        if src <= i < src + rng:
            return tgt + (i - src)
    return i


def get_tables(lines):
    nlines = len(lines)
    block_bounds = [0] + [iline for iline, line in zip(range(nlines), lines) if line == ""] + [nlines]
    tables = []
    for i0, i1 in zip(block_bounds[1:-1], block_bounds[2:]):
        block = [[int(elem) for elem in line.split()] for line in lines[i0 + 2:i1]]
        tables.append(sorted(block, key=lambda x: x[1]))
    return tables


def solve(txt):
    lines = txt.splitlines()
    seed_ids = get_seed_ids(lines)
    location_ids = []
    for seed_id in seed_ids:
        i = seed_id
        for table in get_tables(lines):
            i = apply_table(table, i)
        location_ids.append(i)
    return min(location_ids)


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
