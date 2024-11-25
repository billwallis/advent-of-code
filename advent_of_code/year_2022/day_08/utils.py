"""
Helpful objects to use to solve the day 8 problem.
"""

from typing import Any


def directional_score(directed_list: list, value: int) -> int:
    """
    Calculate the directional score of a given value in a given list.

    The directional score is the number of elements in the list that are less
    than the given value, until the first element that is greater than or equal
    to the given value is encountered.

    :param directed_list: A directed list of integers.
    :param value: An integer value to find the directional score of in the list.
    :return: The directional score of the given value in the given list.
    """
    counter = 0
    for item in directed_list:
        counter += 1
        if item >= value:
            break
    return counter


def split_list_at_index(list_: list, index_: int) -> list[list, Any, list]:
    """
    Split a list at an index.

    This returns a list containing a list, and item, and another list where:

    - The first list contains the items before the item at the index
    - The item is the item at the index
    - The last list contains the items after the item at the index

    Either (or both) of the inner lists can be empty.

    :param list_: The list to split.
    :param index_: The index position to split the list at.
    :return: A list containing a list, and item, and another list.
    """
    return [
        list_[:index_],
        list_[index_],
        list_[1 + index_ :],
    ]


def chained_get(container: dict | list, *args, default: Any = None) -> Any:
    """
    Get a value nested in a container by its nested path.

    :param container: The container to search, either a dictionary or list.
    :param args: The keys or indexes to search for, in order.
    :param default: The value to return if the nested path does not exist.
     Defaults to ``None``.
    :return: The value in the container at the nested path.
    """
    if isinstance(container, list):
        return _chained_get_for_list(container, *args, default=default)
    elif isinstance(container, dict):
        return _chained_get_for_dict(container, *args, default=default)
    else:
        raise TypeError(f"Expected type list or dict, found {container}")


def _chained_get_for_list(multi_list: list, *args, default: Any = None) -> Any:
    """
    Get a value nested in a list of lists by its nested path of indexes.

    :param multi_list: The list of lists to search.
    :param args: The keys to search for, in order.
    :param default: The value to return if the nested path does not exist.
     Defaults to ``None``.
    :return: The value in the multi_list at the nested path.
    """
    value_path = list(args)
    list_chain = multi_list
    while value_path:
        try:
            list_chain = list_chain[value_path.pop(0)]
        except TypeError:
            return default

    return list_chain


def _chained_get_for_dict(dictionary: dict, *args, default: Any = None) -> Any:
    """
    Get a value nested in a dictionary by its nested path.

    :param dictionary: The dictionary to search.
    :param args: The keys to search for, in order.
    :param default: The value to return if the nested path does not exist.
     Defaults to ``None``.
    :return: The value in the dictionary at the nested path.
    """
    value_path = list(args)
    dict_chain = dictionary
    while value_path:
        try:
            dict_chain = dict_chain.get(value_path.pop(0))
        except AttributeError:
            return default

    return dict_chain
