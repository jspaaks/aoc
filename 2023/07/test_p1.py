"""
https://adventofcode.com/2023/day/7
"""
from collections import Counter
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", 6440),
        ("input.txt", 250120186),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_records(lines):
    class Hand:
        order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

        def __init__(self, s):
            self.s = s
            self.counts = sorted(Counter(s).values(), reverse=True)

        @property
        def typ(self):
            if self.counts[0] == 5:
                # Five of a kind
                return 6
            elif self.counts[0] == 4:
                # Four of a kind
                return 5
            elif self.counts[0] == 3:
                if self.counts[1] == 2:
                    # Full house
                    return 4
                # Three of a kind
                return 3
            elif self.counts[0] == 2:
                if self.counts[1] == 2:
                    # Two pairs
                    return 2
                # One pair
                return 1
            elif self.counts[0] == 1:
                # High card
                return 0
            else:
                print("Shouldnt happen")

        def __str__(self):
            types = {
                0: "High card",
                1: "One pair",
                2: "Two pairs",
                3: "Three of a kind",
                4: "Full House",
                5: "Four of a kind",
                6: "Five of a kind",
            }
            return f"{self.s}: {types[self.typ]}"

        def __gt__(self, other):
            if self.typ != other.typ:
                return self.typ > other.typ
            for i in range(5):
                rank_self = Hand.order.index(self.s[i])
                rank_other = Hand.order.index(other.s[i])
                if rank_self != rank_other:
                    return rank_self > rank_other
            return False

    def split(line):
        parts = line.split(None, 1)
        return Hand(parts[0]), int(parts[1])
    return [split(line) for line in lines]


def solve(txt):
    lines = txt.splitlines()
    records = get_records(lines)
    records.sort(key=lambda elem: elem[0], reverse=True)
    n = len(records)
    values = [(b * i) for (_, b), i in zip(records, range(n, 0, -1))]
    return sum(values)


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
