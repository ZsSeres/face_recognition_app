from numpy import random
from typing import List


DEFAULT_FIRST_NAMES: List[str] = []
DEFAULT_LAST_NAMES: List[str] = []

def name_generator(first_names: List[str]=DEFAULT_FIRST_NAMES, last_names: List[str]=DEFAULT_LAST_NAMES)->str:
    """Generates a random name from the given set of first and last names."""


    def __create_list_idx(lst:List)->int:
        return int(random.random()*len(lst))

    first_name_idx = __create_list_idx(first_names)
    last_name_idx = __create_list_idx(last_names)

    first_name = first_name[first_name_idx]
    last_name = last_name[last_name_idx]

    return f"{first_name} {last_name}"