import itertools
import operator
import collections

from iter2.utils import alias_for, define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin_map = map
builtin_sorted = sorted
builtin_zip = zip


itertools_chain_from_iterable = itertools.chain.from_iterable
itertools_product = itertools.product

collections_Counter = collections.Counter
operator_itemgetter = operator.itemgetter


@export_from_module
@alias_for(itertools_product)
def cartesian_product(*iterables, repeat=1):
    '''
    Builds cartesian product from iterables. Alias for itertools::product.

    :param iterables:
    :param repeat:  number of `iterables` repetitions to use
    :return:  iterator through `tuples` from cartesian product of `iterables`
    '''
    pass


@export_from_module
def sort_together(*iterables, key_list=(0,), key_func=None, reverse=False):
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
    if key_func is None:
        key = operator_itemgetter(*key_list)
    else:
        if len(key_list) == 1:
            idx = key_list[0]
            key = lambda item: key_func(item[idx])
        else:
            base_key = operator_itemgetter(*key_list)
            key = lambda item: key_func(*base_key(item))
    return builtin_zip(
        *builtin_sorted(
            builtin_zip(*iterables),
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
    unique_by_iterable = tuple(builtin_map(frozenset, iterables))
    counted = collections_Counter(itertools_chain_from_iterable(unique_by_iterable))
    unique_to_each = frozenset(item for item, count in counted.items() if count == 1)
    return (
        tuple(unique_to_each & it)
        for it in unique_by_iterable
    )

