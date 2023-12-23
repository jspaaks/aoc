"""
https://adventofcode.com/2023/day/8
"""
import re
import math


def get_choices(lines):
    choices = [{"L": 0, "R": 1}[elem] for elem in list(lines[0])]
    return choices, len(choices)


def get_nodes(lines):
    tuples = [re.match(r'([12A-Z]+) = \(([12A-Z]+), ([12A-Z]+)\).*', line).groups() for line in lines[2:]]
    starts = {t[0] for t in tuples if t[0][-1] == "A"}
    return starts, {t[0]: (t[1], t[2]) for t in tuples}


def solve(txt):
    lines = txt.splitlines()
    choices, nchoices = get_choices(lines)
    _, nodes = get_nodes(lines)
    results = []
    paths = [('LJA', 22199), ('NFA', 12083), ('JXA', 17141), ('AAA', 16579), ('PLA', 19951), ('KTA', 14893)]
    starts = {"LJA", "NFA", "JXA", "KTA"}
    n = math.lcm(*[n for name, n in paths if name in starts])
    print(f"n={n}")
    for name in starts:
        for ifollow in range(n):
            choice = choices[ifollow % nchoices]
            name = nodes[name][choice]
        results.append(name)
        print(results)
    return results


if __name__ == "__main__":
    fname = __file__.replace("test_p2_3.py", "input.txt")
    with open(fname, "rt") as fid:
        txt = fid.read()
    solve(txt)
