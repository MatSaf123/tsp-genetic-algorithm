from dataclasses import dataclass
from typing import List
from src.models.ScoredCharacter import ScoredCharacter


@dataclass
class Population:
    # characters: List[Union[List[int], int]]
    characters: List[ScoredCharacter]
