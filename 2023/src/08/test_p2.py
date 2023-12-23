"""
https://adventofcode.com/2023/day/8
"""
import math
import re
import pytest


def get_data():
    ret = []
    testdata = [
        ("example3.txt", 6),
        ("input.txt", None),  # slow
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_choices(lines):
    choices = [{"L": 0, "R": 1}[elem] for elem in list(lines[0])]
    return choices, len(choices)


def get_nodes(lines):
    tuples = [re.match(r'([12A-Z]+) = \(([12A-Z]+), ([12A-Z]+)\).*', line).groups() for line in lines[2:]]
    starts = {t[0] for t in tuples if t[0][-1] == "A"}
    ends = {t[0] for t in tuples if t[0][-1] == "Z"}
    return starts, ends, {t[0]: (t[1], t[2]) for t in tuples}


def solve(txt):
    lines = txt.splitlines()
    choices, nchoices = get_choices(lines)
    currents, ends, nodes = get_nodes(lines)

    ifollow = 0
    while not currents.issubset(ends):
        choice = choices[ifollow % nchoices]
        currents = {nodes[name][choice] for name in currents}
        ifollow += 1
        o = math.log10(ifollow)
        if o % 1 == 0:
            print(f"1e{int(o)}")
    return ifollow


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
