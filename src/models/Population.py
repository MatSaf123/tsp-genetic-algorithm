from dataclasses import dataclass
from typing import List, Union


@dataclass
class Population:
    characters: List[Union[List[int], int]]
