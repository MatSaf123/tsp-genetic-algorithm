from dataclasses import dataclass
from typing import List


@dataclass
class ScoredCharacter:
    genotype: List[int]
    score: int
