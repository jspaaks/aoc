"""
https://adventofcode.com/2023/day/1
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example-1.txt", sum([12, 38, 15, 77])),
        ("input.txt", 55090),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def solve(txt):
    lines = txt.splitlines()
    numerals = {str(item) for item in range(0, 10)}
    numbers_only = [[c for c in line if c in numerals] for line in lines]
    return sum([int("".join([elem[0], elem[-1]])) for elem in numbers_only])


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert expected == solve(txt)
