import csv
import random
from typing import List

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


def generate_random_population(distances_matrix: List[List[int]], seed: int = None):
    if seed is not None:
        random.seed(seed)
    characters = []
    for _ in range(len(distances_matrix)):
        temp_slice = []
        for _ in range(len(distances_matrix)):
            index_unique = False
            while not index_unique:
                random_index = get_random_index(1, len(distances_matrix))
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
            temp_sum += distances_matrix[i][character_index - 1]
        scores.append(temp_sum)
        temp_sum = 0
    return scores
