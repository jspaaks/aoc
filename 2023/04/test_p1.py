"""
https://adventofcode.com/2023/day/4
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", sum([8, 2, 2, 1, 0, 0])),
        ("input.txt", 24706),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def calc_score(line):
    numbers = line.split(":", maxsplit=1)[1]
    winning_str, have_str = numbers.split("|")
    winning = {int(elem) for elem in winning_str.split()}
    have = {int(elem) for elem in have_str.split()}
    overlap = len(winning.intersection(have))
    return 2**(overlap - 1) if overlap >= 1 else 0


def solve(txt):
    lines = txt.splitlines()
    return sum([calc_score(line) for line in lines])


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
