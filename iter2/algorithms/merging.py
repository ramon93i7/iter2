import itertools

from iter2.utils import alias_for, define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin_zip = zip

itertools_chain = itertools.chain
itertools_chain_from_iterable = itertools.chain.from_iterable
itertools_cycle = itertools.cycle
itertools_islice = itertools.islice
itertools_repeat = itertools.repeat
itertools_zip_longest = itertools.zip_longest


@export_from_module
@alias_for(itertools_chain)
def chain(*iterables):
    '''
    Returns a new iterable yielding items from `iterables`, iterable by iterable.

    :param iterables:
    :return:  chained iterables as new iterable

    Example:
    >>> list(chain([1, 2], 'ab'))
    [1, 2, 'a', 'b']

    See also `chain_from_iterable`
    '''
    pass


@export_from_module
@alias_for(itertools_chain_from_iterable)
def chain_from_iterable(iterables_in_iterable):
    '''
    Returns a new iterable yielding items from iterables, iterable by iterable.
    This is the same as `chain` b   ut consumes iterables from another iterable.

    :param iterables_in_iterable:
    :return:  chained iterables as new iterable

    Example:
    >>> list(chain_from_iterable(['ab', 'cd', 'ef']))
    ['a', 'b', 'c', 'd', 'e', 'f']
    '''
    pass


@export_from_module
def interleave(*iterables):
    '''
    Returns a new iterable yielding from each iterable in turn, until the longest is exhausted.

    :param iterables:
    :return:

    Example:
    >>> interleave([1, 2], 'abc')
    [1, 'a', 2, 'b', 'c']
    '''
    # TODO: think about better solution
    MISSING_MARK = object()  # truly unique value
    return (
        item
        for item in itertools_chain_from_iterable(itertools_zip_longest(*iterables, fillvalue=MISSING_MARK))
        if item is not MISSING_MARK
    )


@export_from_module
def interleave_shortest(*iterables):
    '''
    Returns a new iterable yielding from each iterable in turn, until the shortest is exhausted.

    :param iterables:
    :return:  iterable

    Example:
    >>> interleave_shortest([1, 2], 'abc')
    [1, 'a', 2, 'b']
    '''
    # TODO: think about better solution
    return itertools_chain_from_iterable(builtin_zip(*iterables))


@export_from_module
def prepend(iterator, another_iterator):
    '''
    Returns a new iterable, alias for `chain(another_iterator, iterator)`.
    First, yields items from `another_iterator`, then from `iterator`.

    :param iterator:
    :param another_iterator:
    :return:  iterable

    Example:
    >>> tuple(prepend([4, 5, 6], [1, 2, 3]))
    (1, 2, 3, 4, 5, 6)
    '''
    return itertools_chain(another_iterator, iterator)


@export_from_module
@alias_for(interleave)
def roundrobin(*iterables):
    pass


@export_from_module
@alias_for(builtin_zip)
def zip(*iterables):
    pass


@export_from_module
@alias_for(itertools_zip_longest)
def zip_longest(*iterables, fillvalue=None):
    pass


@export_from_module
def zip_offset(*iterables, offsets, fillvalue=None, longest=False):
    '''
    `zip` the input `iterables` together, but offset the i-th iterable by the i-th item in `offsets`.

    :param iterables:
    :param offsets:
    :param fillvalue:  fillvalue for longest=True case
    :param longest:  if `True` iterates until longest iterable exhausted
    :return:  tuples with zipped items

    Example:
    >>> tuple(zip_offset('123', 'abcde', offsets=(0, 1)))
    (('1', 'b'), ('2', 'c'), ('3', 'd'))
    >>> tuple(zip_offset('123', 'abcde', offsets=(0, 1), fillvalue='#', longest=True))
    (('1', 'b'), ('2', 'c'), ('3', 'd'), ('#', 'e'))
    '''
    # based on more-itertools::zip_offset
    if len(iterables) != len(offsets):
        raise ValueError("Number of iterables and offsets didn't match")

    staggered = []
    add_to_staggered = staggered.append
    for it, n in builtin_zip(iterables, offsets):
        if n < 0:
            add_to_staggered(
                itertools_chain(
                    itertools_repeat(fillvalue, -n),
                    it
                )
            )
        elif n > 0:
            add_to_staggered(itertools_islice(it, n, None))
        else:
            add_to_staggered(it)

    if longest:
        return itertools_zip_longest(*staggered, fillvalue=fillvalue)
    else:
        return builtin_zip(*staggered)

