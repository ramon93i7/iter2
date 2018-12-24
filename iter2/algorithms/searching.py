from iter2.utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


builtin_enumerate = enumerate
builtin_filter = filter


@export_from_module
def find(iterable, predicate):
    '''
    Yields first occurrence of item for which `predicate` is True

    :param iterable:
    :param predicate:
    :return:

    Example:
    >>> find([1, 2, 3], lambda x: x % 2 == 0)
    2
    '''
    return next(builtin_filter(predicate, iterable))


@export_from_module
def locate(iterable, predicate, *, count_from=0, with_items=False):
    '''
    Searches items for which `predicate` is True. Yields indexes started from `count_from`.
    If `with_items` is True then yields tuples (index, item)

    :param iterable:
    :param predicate:
    :param count_from:
    :param with_items:
    :return:  indexes  or  (index, item),...

    Example:
    >>> tuple(locate([1, 2, 3, 4, 5], lambda x: x % 2 == 0, count_from=1))
    (2, 4)
    >>> tuple(locate(['aBcDe'], str.isupper, with_items=True))
    ((1, 'B'), (3, 'D'))
    '''

    if with_items:
        return (
            (idx, item)
            for idx, item in builtin_enumerate(iterable, count_from)
            if predicate(item)
        )
    else:
        return (
            idx
            for idx, item in builtin_enumerate(iterable, count_from)
            if predicate(item)
        )


@export_from_module
def position(iterable, predicate, *, count_from=0):
    '''
    Returns index (starting from `count_from`) of first occurrence of item for which `predicate` is True.
    If `predicate` is False for all items returns -1.

    :param iterable:
    :param predicate:
    :param count_from:
    :return:  index   or  -1

    Example:
    >>> position('aBcD', str.isupper, count_from=1)
    2
    >>> position('abcd', str.isupper, count_from=1)
    -1
    '''
    return next(locate(iterable, predicate, count_from=count_from), -1)

