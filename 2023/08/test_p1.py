"""
https://adventofcode.com/2023/day/8
"""
import re
import pytest


def get_data():
    ret = []
    testdata = [
        ("example1.txt", 2),
        ("example2.txt", 6),
        ("input.txt", 16579),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_choices(lines):
    choices = [{"L": 0, "R": 1}[elem] for elem in list(lines[0])]
    return choices, len(choices)


def get_nodes(lines):
    tuples = [re.match(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\).*', line).groups() for line in lines[2:]]
    tuples.sort(key=lambda t: t[0])
    return tuples[0][0], tuples[-1][0], {t[0]: (t[1], t[2]) for t in tuples}


def solve(txt):
    lines = txt.splitlines()
    choices, nchoices = get_choices(lines)
    start_node, final_node, nodes = get_nodes(lines)
    node = start_node

    ifollow = 0
    while node != final_node:
        choice = choices[ifollow % nchoices]
        node = nodes[node][choice]
        ifollow += 1
    return ifollow


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
