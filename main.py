import csv
from operator import attrgetter
import random
from typing import List

from src.models.Population import Population
from src.models.ScoredCharacter import ScoredCharacter
from src.models.utils import add_at_first_found_none

# TODO: move this away from main.py


def read_from_file(path: str, delimiter=" ") -> List[List[str]]:
    with open(path, newline="") as file:
        return [
            list(filter(None, row)) for row in csv.reader(file, delimiter=delimiter)
        ]


def create_distances_matrix(data: List[List[int]]) -> List[List[int]]:
    size = int(data[0][0])
    matrix = [[None] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            try:
                matrix[x][y] = int(data[x + 1][y])
            except IndexError:
                matrix[x][y] = int(data[y + 1][x])
    return matrix


def get_random_index(min: int, max: int) -> int:
    """Inclusive for both min and max"""
    return random.randint(min, max)


def generate_random_population(n: int, seed: int = None) -> List[List[int]]:
    if seed is not None:
        random.seed(seed)
    characters = []
    for _ in range(n):
        temp_slice = []
        for _ in range(n):
            index_unique = False
            while not index_unique:
                random_index = get_random_index(0, n - 1)
                if random_index not in temp_slice:
                    index_unique = True
            temp_slice.append(random_index)
        characters.append(temp_slice)
        temp_slice = None
    return characters


def get_scores_for_population(
    distances_matrix: List[List[int]], characters_matrix: List[List[int]]
) -> List[int]:
    scores = []
    char_len = len(characters_matrix[0])
    for character in characters_matrix:
        char_score = 0
        for i in range(char_len - 1):
            char_score += distances_matrix[character[i]][character[i + 1]]
        char_score += distances_matrix[character[-1]][character[0]]
        scores.append(char_score)
    return scores


def get_population_with_scores(path: str) -> Population:
    distances_matrix = create_distances_matrix(read_from_file(path))
    characters = generate_random_population(len(distances_matrix))
    scores = get_scores_for_population(distances_matrix, characters)
    return Population(
        [ScoredCharacter(characters[i], scores[i]) for i in range(len(scores))]
    )


def run_tournament_selection(population: Population, k: int, n: int) -> Population:
    """
    k: selective pressure value
    n: population size
    """
    return Population(
        [
            min(random.sample(population.characters, k), key=attrgetter("score"))
            for _ in range(n)
        ]
    )


def run_proportional_selection(population: Population, n: int) -> Population:
    """
    n: population size
    """
    scores = [sc.score for sc in population.characters]
    max_score = max(scores)
    new_scores = [max_score + 1 - score for score in scores]
    p_sum = sum(new_scores)
    probabilities = [p / p_sum for p in new_scores]
    return Population(random.choices(population.characters, probabilities, k=n))


def ox_cross(
    population: Population, genotype_len: int, a: int = None, b: int = None, chance: int = 0.5
) -> Population:

    new_characters: List[List[int]] = []
    for parent_a, parent_b in zip(
        population.characters[0::2], population.characters[1::2]
    ):
        if random.uniform(0, 1) < chance:
            new_characters.extend([parent_a.genotype, parent_b.genotype])
            continue

        if a is None or b is None:
            break_points = list(range(1, genotype_len))
            a = random.choice(break_points)
            break_points.pop(a - 1)
            b = random.choice(break_points)
            a, b = sorted([a, b])

        lefts = parent_a.genotype[:a], parent_b.genotype[:a]
        middles = parent_a.genotype[a:b], parent_b.genotype[a:b]
        rights = parent_a.genotype[b:], parent_b.genotype[b:]

        children = [[None] * genotype_len, [None] * genotype_len]
        for i, c in enumerate(children):
            c[a:b] = middles[i]

        work_lists = [rights[i] + lefts[i] + middles[i] for i in range(2)]
        work_lists.reverse()

        for i, child in enumerate(children):
            for j in range(genotype_len):
                if work_lists[i][j] in child:
                    continue
                else:
                    add_at_first_found_none(child, work_lists[i][j])
        new_characters.extend(children)

    # we don't need to compute score at this point
    return Population([ScoredCharacter(nc, 0) for nc in new_characters])


def swap_mutate(population: Population, genotype_len: int, chance: int = 0.5) -> Population:

    for character in population.characters:
        if random.uniform(0, 1) < chance:
            continue

        for a in range(genotype_len):
            b = get_random_index(0, genotype_len - 1)
            while a == b:
                b = get_random_index(0, genotype_len - 1)
            temp = character.genotype[a]
            character.genotype[a] = character.genotype[b]
            character.genotype[b] = temp
    return population


def run_simple_genetic_algorithm(path: str, epochs: int = 100) -> None:
    t = 0
    population: Population = get_population_with_scores(path)
    n = len(population.characters)
    k = 32
    genotype_len = len(population.characters[0].genotype)
    distances_matrix = create_distances_matrix(read_from_file(path))
    min_global = min(random.sample(population.characters, k), key=attrgetter("score"))

    while t < epochs:
        print(f"Running iteration: {t}")
        population_t = run_tournament_selection(population, k, n)
        # population_t = run_proportional_selection(population, n)
        population_o = ox_cross(population_t, genotype_len)
        population_o = swap_mutate(population_o, genotype_len)
        scores = get_scores_for_population(
            distances_matrix,
            [character.genotype for character in population_o.characters],
        )
        population.characters = population_o.characters
        for i, character in enumerate(population.characters):
            character.score = scores[i]

        min_local = min(random.sample(population.characters, k), key=attrgetter("score"))
        print("min_local:", min_local.score)
        if min_local.score < min_global.score:
            min_global = min_local
        t += 1

    print("min_global:", min_global.score)
