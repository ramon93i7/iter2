import itertools
import operator
import collections

from iter2.utils import alias_for, define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin__map = map
builtin__sorted = sorted
builtin__zip = zip


itertools__chain_from_iterable = itertools.chain.from_iterable
itertools__product = itertools.product

collections__Counter = collections.Counter
operator__itemgetter = operator.itemgetter


UNDEFINED = object()


@export_from_module
@alias_for(itertools__product)
def cartesian_product(*iterables, repeat=1):
    '''
    Builds cartesian product from iterables. Alias for itertools::product.

    :param iterables:
    :param repeat:  number of `iterables` repetitions to use
    :return:  iterator through `tuples` from cartesian product of `iterables`
    '''
    pass


@export_from_module
def sort_together(*iterables, key_list=(0,), key_func=UNDEFINED, reverse=False):
    '''
    Sorts iterables as they were zipped.

    :param iterables:
    :param key_list:   indexes of iterators which items are used in `key_func`
    :param key_func:  function to calculate a key
    :param reverse:  descending sort order if True
    :return:  iterator of iterators (count = len(iterables))

    Example:
    >>> tuple(map(tuple, sort_together([1, 2, 3, 4, 5], 'abcde', key_func=(lambda x: x % 2))))
    ((2, 4, 1, 3, 5), ('b', 'd', 'a', 'c', 'e'))
    '''
    if key_func is UNDEFINED:
        key = operator__itemgetter(*key_list)
    else:
        # TODO: simplify and test performance
        if len(key_list) == 1:
            idx = key_list[0]
            key = lambda item: key_func(item[idx])
        else:
            base_key = operator__itemgetter(*key_list)
            key = lambda item: key_func(*base_key(item))
    return builtin__zip(
        *builtin__sorted(
            builtin__zip(*iterables),
            key=key,
            reverse=reverse
        )
    )


@export_from_module
def unique_to_each(*iterables):
    '''
    Searches items which are contained by one iterable only. Order of items in result can differ from original.

    :param iterables:
    :return:  iterator of tuples with unique-to-each items per iterable

    Example:
    >>> tuple(unique_to_each((1, 2, 3), (3, 4, 5), (5, 6, 7)))
    ((1,), (4,), (7,))
    '''
    unique_by_iterable = tuple(builtin__map(frozenset, iterables))
    counted = collections__Counter(itertools__chain_from_iterable(unique_by_iterable))
    unique_to_each = frozenset(item for item, count in counted.items() if count == 1)
    return (
        tuple(unique_to_each & it)
        for it in unique_by_iterable
    )

