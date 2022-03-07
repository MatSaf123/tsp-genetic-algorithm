import csv
from typing import List

# TODO: move this away from main.py


def read_from_file(path: str, delimiter=" ") -> List[any]:
    with open(path, newline="") as file:
        return [row for row in csv.reader(file, delimiter=delimiter)]


def create_matrix(data: List[List[int]]) -> List[List[int]]:
    size = int(data[0][0])
    matrix = [[None] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            try:
                matrix[x][y] = data[x + 1][y]
            except IndexError:
                matrix[x][y] = data[y + 1][x]
    return matrix
