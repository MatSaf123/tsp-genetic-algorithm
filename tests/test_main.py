from main import generate_random_population, read_from_file, create_distances_matrix


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


def test_create_distances_matrix():
    expected = [
        ["0", "1", "4", "7", "9"],
        ["1", "0", "2", "2", "1"],
        ["4", "2", "0", "5", "7"],
        ["7", "2", "5", "0", "8"],
        ["9", "1", "7", "8", "0"],
    ]
    assert create_distances_matrix(read_from_file("data/test.txt")) == expected


def test_generate_random_population():
    matrix = create_distances_matrix(read_from_file("data/test.txt"))
    expected = [
        [1, 3, 4, 5, 2],
        [2, 3, 5, 1, 4],
        [1, 5, 4, 3, 2],
        [2, 1, 3, 4, 5],
        [4, 3, 1, 5, 2],
    ]
    assert generate_random_population(matrix, 123) == expected
