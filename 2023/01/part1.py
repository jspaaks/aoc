def solve(data_in):
    numeric = {str(item) for item in range(0, 10)}
    numbers_only = [[c for c in line if c in numeric] for line in data_in]
    return sum([int("".join([elem[0], elem[-1]])) for elem in numbers_only])


def test_example():
    data_in = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]
    data_out = sum([
        12, 38, 15, 77
    ])
    assert data_out == solve(data_in)


if __name__ == "__main__":
    with open("input.txt", "rt") as fid:
        lines = fid.readlines()
    print(solve(lines))
