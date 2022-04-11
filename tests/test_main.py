import random
from main import (
    generate_random_population,
    get_scores_for_population,
    read_from_file,
    create_distances_matrix,
    get_population_with_scores,
    run_proportional_selection,
    run_simple_genetic_algorithm,
    ox_cross,
    run_tournament_selection,
    swap_mutate,
)
from src.models.Population import Population
from src.models.ScoredCharacter import ScoredCharacter


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
    expected = [
        [0, 2, 3, 4, 1],
        [1, 2, 4, 0, 3],
        [0, 4, 3, 2, 1],
        [1, 0, 2, 3, 4],
        [3, 2, 0, 4, 1],
    ]
    assert generate_random_population(5, 5, 123) == expected
    assert generate_random_population(5, 5, 321) != expected


def test_get_scores_for_population():
    distances_matrix = create_distances_matrix(read_from_file("data/test.txt"))

    sample_population = [[0, 1, 2, 3, 4]]
    ret = get_scores_for_population(distances_matrix, sample_population)
    assert ret == [25]

    characters_matrix = generate_random_population(len(distances_matrix), 5, 123)
    expected = [19, 27, 25, 19, 21]
    assert get_scores_for_population(distances_matrix, characters_matrix) == expected
    characters_matrix_2 = generate_random_population(len(distances_matrix), 5, 321)
    assert characters_matrix != characters_matrix_2
    assert get_scores_for_population(distances_matrix, characters_matrix_2) != expected


def test_run_tournament_selection():
    random.seed(10)
    population = get_population_with_scores("data/test.txt", 5)
    ret = run_tournament_selection(population, 3, 5)
    expected = [
        [4, 0, 3, 1, 2],
        [0, 1, 2, 3, 4],
        [1, 0, 4, 3, 2],
        [1, 0, 4, 3, 2],
        [0, 1, 2, 3, 4],
    ]
    for i, character in enumerate(ret.characters):
        character.genotype == expected[i]


def test_run_proportional_selection():
    random.seed(666)
    population = get_population_with_scores("data/test.txt", 5)
    ret = run_proportional_selection(population, 5)
    expected = [
        [3, 4, 1, 0, 2],
        [3, 4, 1, 0, 2],
        [3, 2, 4, 0, 1],
        [0, 2, 1, 4, 3],
        [3, 4, 1, 0, 2],
    ]
    for i, character in enumerate(ret.characters):
        character.genotype == expected[i]


def test_ox_cross():
    parent_a = [0, 1, 2, 3, 4, 5, 6]
    parent_b = [4, 5, 1, 0, 3, 2, 6]
    population = Population(
        [ScoredCharacter(parent_a, 0), ScoredCharacter(parent_b, 0)]
    )
    result = ox_cross(population, 7, 2, 5, 1)
    assert [result.characters[0].genotype, result.characters[1].genotype] == [
        [6, 5, 2, 3, 4, 1, 0],
        [5, 6, 1, 0, 3, 2, 4],
    ]


def test_run():
    random.seed(None)
    run_simple_genetic_algorithm("data/berlin52.txt", 5, 200, 0.75, 0.05, 1000)
