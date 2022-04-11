from typing import List

from ..models.ScoredCharacter import ScoredCharacter


def add_at_first_found_none(l: List[any], value: any) -> List[any]:
    for i, ele in enumerate(l):
        if ele is None:
            l[i] = value
            return l
    raise Exception("Did not find any None values in list to replace with new value.")


def print_result(result: ScoredCharacter) -> None:
    res_str = "-".join([f"{g}" for g in result.genotype])
    print("\n", res_str, result.score, "\n")
