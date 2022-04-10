from dataclasses import dataclass
from typing import List, Union


@dataclass
class ScoredCharacter:
    genotype: List[int]
    score: int
