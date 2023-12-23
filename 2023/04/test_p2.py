"""
https://adventofcode.com/2023/day/4
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", sum([1, 2, 4, 8, 14, 1])),
        ("input.txt", 13114317),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def calc_overlap(line):
    numbers = line.split(":", maxsplit=1)[1]
    winning_str, have_str = numbers.split("|")
    winning = {int(elem) for elem in winning_str.split()}
    have = {int(elem) for elem in have_str.split()}
    return len(winning.intersection(have))


def solve(txt):
    lines = txt.splitlines()
    overlap = [calc_overlap(line) for line in lines]
    ncopies = [1 for _ in lines]
    for iline, _ in enumerate(lines):
        for k in range(overlap[iline]):
            ncopies[iline + 1 + k] += ncopies[iline]
    return sum(ncopies)


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
