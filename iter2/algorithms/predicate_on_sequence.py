from iter2.utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin_all = all
builtin_any = any
builtin_map = map


@export_from_module
def all(iterable, predicate):
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
    return builtin_all(builtin_map(predicate, iterable))


@export_from_module
def any(iterable, predicate):
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
    return builtin_any(builtin_map(predicate, iterable))


@export_from_module
def none(iterable, predicate):
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
    return not builtin_any(builtin_map(predicate, iterable))

