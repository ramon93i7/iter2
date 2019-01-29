import functools
import operator

from iter2.utils import alias_for, define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin_sum = sum
builtin_max = max
builtin_min = min

functools_reduce = functools.reduce
operator_mul = operator.mul


@export_from_module
def count(iterable):
    '''
    Counts number of items in iterable.

    :param iterable:
    :return:  number of items in `iterable`

    Example:
    >>> count([1, 2, 3])
    3
    '''
    return builtin_sum(1 for _ in iterable)


@export_from_module
def fold(iterable, func, *, initial=None):
    '''
    Apply a function `func` of two arguments cumulatively to the items of a `iterable`,
    from left to right, so as to reduce the sequence to a single value. If `initial` is not None
    then it is used as the first state value.

    :param iterable:
    :param func:  (state_value, next_item) -> new_state_value
    :param initial:  optional first state value
    :return:  cumulative value

    Example:
    >>> fold([1, 2, 3, 4, 5], lambda state, item: state * item)
    120
    '''
    if initial is None:
        return functools_reduce(func, iterable)
    else:
        return functools_reduce(func, iterable, initial)


@export_from_module
def join(iterable, sep):
    '''
    Concatenates strings from `iterator` with `sep` between adjacent items.

    :param iterable:
    :param sep:   separator
    :return:  concatenated string

    Example:
    >>> join(['555', '404', '42', '73'], '-')
    '555-404-42-73'
    '''
    # TODO: use only when type hints are available
    return sep.join(iterable)


@export_from_module
def max(iterable, *, default=None, key=None):
    '''
    Returns biggest item from iterable. If iterable is empty returns None.
    If `key` function is set then `key(item)` is used as value for comparison.

    :param iterable:
    :param default:  default value to return if iterable is empty
    :param key:  function to calculate comparison key
    :return:  biggest item

    Example:
    >>> max([1, 2, 3])
    3
    >>> max([1, 2, 3], key=lambda x: x % 3)
    2
    >>> max([], default='nothing')
    'nothing'
    '''
    if key is None:
        return builtin_max(iterable, default=default)
    else:
        return builtin_max(iterable, default=default, key=key)


@export_from_module
def min(iterator, *, default=None, key=None):
    '''
    Returns smallest item from iterable. If iterable is empty returns None.
    If `key` function is set then `key(item)` is used as value for comparison.

    :param iterator:
    :param default:  default value to return if iterable is empty
    :param key:  function to calculate comparison key
    :return:  smallest value

    Example:
    >>> min([1, 2, 3])
    1
    >>> min([1, 2, 3], key=lambda x: x % 3)
    3
    >>> min([], default='nothing')
    'nothing'
    '''
    if key is None:
        return builtin_min(iterator, default=default)
    else:
        return builtin_min(iterator, default=default, key=key)


@export_from_module
def minmax(iterable, *, default=None, key=None):
    '''
    Returns smallest and biggest item from iterable. If iterable is empty returns `None`.
    If `key` function is set then `key(item)` is used as value for comparison.

    :param iterable:
    :param default:  default value to return if iterable is empty
    :param key:  function to calculate comparison key
    :return:  (smallest item, biggest item)

    Example:
    >>> minmax([1, 2, 3])
    (1, 3)
    >>> minmax([1, 2, 3], key=lambda x: x % 3)
    (3, 2)
    >>> minmax([], default='nothing')
    'nothing'
    '''
    # TODO: search for more optimized algo
    iterator = iter(iterable)
    if key is None:  # w/o key
        try:
            first = next(iterator)
            min_element = first
            max_element = first
        except StopIteration:
            return default

        for item in iterator:
            if item < min_element:
                min_element = item
            elif item > max_element:
                max_element = item

        return min_element, max_element

    else:
        try:
            first = next(iterator)
            first_key = key(first)
            min_element, min_key = first, first_key
            max_element, max_key = first, first_key
        except StopIteration:
            return default

        for item in iterator:
            item_key = key(item)
            if item_key < min_key:
                min_element, min_key = item, item_key
            elif item_key > max_key:
                max_element, max_key = item, item_key

        return min_element, max_element


@export_from_module
def product(iterable):
    '''
    Returns the product of items from `iterable`.

    :param iterable:
    :return:  product of items

    Example:
    >>> product([1, 2, 3, 4, 5])
    120
    '''
    return functools_reduce(operator_mul, iterable)


@export_from_module
@alias_for(fold)
def reduce(iterable, func, *, initial=None):
    pass


@export_from_module
def sum(iterable):
    ''''
    Returns the sum of items from `iterable`.

    :param iterable:
    :return:  sum of items

    Example:
    >>> sum([1, 2, 3, 4, 5])
    15
    '''
    return builtin_sum(iterable)
