from typing import List


def add_at_first_found_none(l: List[any], value: any) -> List[any]:
    for i, ele in enumerate(l):
        if ele is None:
            l[i] = value
            return l
    raise Exception("Did not find any None values in list to replace with new value.")
