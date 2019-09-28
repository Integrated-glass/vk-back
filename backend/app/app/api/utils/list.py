from typing import List


def get_from_list_or_default(list: List, index: int, default=None):
    try:
        return list[index]
    except IndexError:
        return default
