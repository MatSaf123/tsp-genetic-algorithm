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
        return [row for row in csv.reader(file, delimiter=delimiter)]


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


def generate_random_population(
    distances_matrix: List[List[int]], seed: int = None
) -> List[List[int]]:
    if seed is not None:
        random.seed(seed)
    characters = []
    for _ in range(len(distances_matrix)):
        temp_slice = []
        for _ in range(len(distances_matrix)):
            index_unique = False
            while not index_unique:
                random_index = get_random_index(0, len(distances_matrix) - 1)
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
    cm_len = len(characters_matrix)
    for i in range(cm_len):
        temp_sum = 0
        for j in range(cm_len):
            character_index = characters_matrix[i][j]
            temp_sum += distances_matrix[i][character_index]
        scores.append(temp_sum)
        temp_sum = 0
    return scores


def get_population_with_scores(path: str) -> Population:
    distances_matrix = create_distances_matrix(read_from_file(path))
    characters = generate_random_population(distances_matrix)
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


def run_proportional_selection(population: Population, k: int, n: int) -> Population:
    """
    k: selective pressure value
    n: population size
    """
    scores = [sc.score for sc in population.characters]
    max_score = max(scores)
    new_scores = [max_score + 1 - score for score in scores]
    p_sum = sum(new_scores)
    probabilities = [p / p_sum for p in new_scores]
    return Population(random.choices(population.characters, probabilities, k=n))


def ox_cross(
    population: Population, genotype_len: int, a: int = None, b: int = None
) -> Population:
    # TODO: implement probability of crossing

    new_characters: List[List[int]] = []
    for parent_a, parent_b in zip(
        population.characters[0::2], population.characters[1::2]
    ):
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


def run_simple_genetic_algorithm(path: str, epochs: int = 100) -> None:
    t = 0
    population: Population = get_population_with_scores(path)
    n = len(population.characters)
    k = 3
    genotype_len = len(population.characters[0].genotype)
    while t < epochs:
        print(f"Running iteration: {t}")
        print("Running selection...")
        population_t = run_tournament_selection(population, k, n)
        # population_t = run_proportional_selection(population, k, n)
        print("Selection done.")
        print("Running crossing...")
        population_o = ox_cross(population_t, genotype_len)
        print("Crossing done.")
        print(f"Finished iteration: {t}")
        t += 1
