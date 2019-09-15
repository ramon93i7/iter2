from iter2.utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin__all = all
builtin__any = any
builtin__map = map


@export_from_module
def all(iterable, predicate) -> bool:
    '''
    Checks if `predicate` is True on every item in `iterator`

    :param iterable:
    :param predicate:
    :return:  True or False

    Example:
    >>> all([1, 2, 3], lambda x: x < 10)
    True
    >>> all([1, 2, 3], lambda x: x % 2 == 0)
    False
    '''
    return builtin__all(builtin__map(predicate, iterable))


@export_from_module
def any(iterable, predicate) -> bool:
    '''
    Checks if `predicate` is True on at least one item in `iterator`

    :param iterable:
    :param predicate:
    :return:  True or False

    Example:
    >>> any([1, 2, 3], lambda x: x > 10)
    False
    >>> any([1, 2, 3], lambda x: x % 2 == 0)
    True
    '''
    # faster than `next(filter(predicate, iterable), False) and True`
    return builtin__any(builtin__map(predicate, iterable))


@export_from_module
def none(iterable, predicate) -> bool:
    '''
    Checks if `predicate` is False on every item in `iterator`

    :param iterable:
    :param predicate:
    :return:  True or False

    Example:
    >>> none([1, 2, 3], lambda x: x < 10)
    True
    >>> none([1, 2, 3], lambda x: x % 2 == 0)
    False
    '''
    return not any(iterable, predicate)

