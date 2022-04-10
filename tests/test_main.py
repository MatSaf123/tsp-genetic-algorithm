from main import (
    generate_random_population,
    get_scores_for_population,
    read_from_file,
    create_distances_matrix,
    get_population_with_scores,
    run_simple_genetic_algorithm,
)


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
        [0, 1, 4, 7, 9],
        [1, 0, 2, 2, 1],
        [4, 2, 0, 5, 7],
        [7, 2, 5, 0, 8],
        [9, 1, 7, 8, 0],
    ]
    assert create_distances_matrix(read_from_file("data/test.txt")) == expected


def test_generate_random_population():
    distances_matrix = create_distances_matrix(read_from_file("data/test.txt"))
    expected = [
        [0, 2, 3, 4, 1],
        [1, 2, 4, 0, 3],
        [0, 4, 3, 2, 1],
        [1, 0, 2, 3, 4],
        [3, 2, 0, 4, 1],
    ]
    assert generate_random_population(distances_matrix, 123) == expected


def test_get_scores_for_population():
    distances_matrix = create_distances_matrix(read_from_file("data/test.txt"))
    characters_matrix = generate_random_population(distances_matrix, 123)
    expected = [21, 6, 18, 22, 25]
    assert get_scores_for_population(distances_matrix, characters_matrix) == expected


# def test_run():
# run_simple_genetic_algorithm("data/test.txt", 1)
