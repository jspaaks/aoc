"""
https://adventofcode.com/2023/day/1
"""
import pytest


numerals = {str(item) for item in range(0, 10)}


def _replace_spelled_outs(lines):
    # wf: word to find, wr: word to replace
    words = [(wf, wr, len(wf)) for wf, wr, in [
        ("one", "1__"),
        ("two", "2__"),
        ("three", "3____"),
        ("four", "4___"),
        ("five", "5___"),
        ("six", "6__"),
        ("seven", "7____"),
        ("eight", "8____"),
        ("nine", "9___"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
    ]]
    # find the first occurrence of spelled out number, replace only that
    replaced = list()
    for line in lines:
        # collect data about the position of all the words -- .index and .rindex are both needed
        # to avoid problems with repeated words within a line
        position_data = \
            [(line.index(wf), wf, wr, wl) for wf, wr, wl in words if wf in line] + \
            [(line.rindex(wf), wf, wr, wl) for wf, wr, wl in words if wf in line]
        # sort position data by index (necessary for avoiding problems with overlapping words
        # like 'oneight')
        position_data.sort(key=lambda elem: elem[0])
        for i in [0, -1]:
            from_pos, _, wr, wl = position_data[i]
            line = line[:from_pos] + wr + line[from_pos + wl:]
        replaced.append(line.replace("_", ""))
    return replaced


def _throw_out_alphas(lines):
    return [[c for c in line if c in numerals] for line in lines]


def solve(txt):
    lines = txt.splitlines()
    lines_no_spelled_outs = _replace_spelled_outs(lines)
    numbers_only = _throw_out_alphas(lines_no_spelled_outs)
    return sum([int("".join([elem[0], elem[-1]])) for elem in numbers_only])


def get_data():
    ret = []
    testdata = [
        ("example-2.txt", sum([29, 83, 13, 24, 42, 14, 76])),
        ("input.txt", 54845),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert expected == solve(txt)
