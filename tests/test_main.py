from main import read_from_file, create_matrix


def test_read_from_file():
    expected = [
        ["5"],
        ["0"],
        ["1", "0"],
        ["4", "2", "0"],
        ["7", "2", "5", "0"],
        ["9", "1", "7", "8", "0"],
    ]
    assert read_from_file("data/test.txt") == expected


def test_create_matrix():
    expected = [
        ["0", "1", "4", "7", "9"],
        ["1", "0", "2", "2", "1"],
        ["4", "2", "0", "5", "7"],
        ["7", "2", "5", "0", "8"],
        ["9", "1", "7", "8", "0"],
    ]
    assert create_matrix(read_from_file("data/test.txt")) == expected
