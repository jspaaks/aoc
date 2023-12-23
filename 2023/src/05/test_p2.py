"""
https://adventofcode.com/2023/day/5
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", 46),
        ("input.txt", 24261545),  # slow
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_seed_id_ranges(lines):
    alternating = [int(elem) for elem in lines[0].split(":", maxsplit=1)[1].strip().split()]
    ranges = [range(start, start + rng) for start, rng in zip(alternating[:-1:2], alternating[1::2])]
    return ranges


def apply_table(table, i):
    for (tgt, src, rng) in table:
        if src > i:
            break
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
    seed_id_ranges = get_seed_id_ranges(lines)
    tables = get_tables(lines)
    location_id = None
    for irange, seed_id_range in enumerate(seed_id_ranges):
        print(f"irange = {irange}")
        for seed_id in seed_id_range:
            i = seed_id
            for table in tables:
                i = apply_table(table, i)
            if location_id is None or i < location_id:
                print(f"intermediate location: {i}")
                location_id = i
    return location_id


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
