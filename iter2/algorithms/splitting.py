import itertools
import operator

from iter2.iterators.spy_iterator import SpyIterator
from iter2.utils import define_module_exporter, Flag


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin_enumerate = enumerate
builtin_filter = filter
builtin_map = map

itertools_filterfalse = itertools.filterfalse
itertools_islice = itertools.islice
itertools_tee = itertools.tee

operator_itemgetter = operator.itemgetter


@export_from_module
def distribute(iterable, n):
    '''
    Distributes items from `iterable` among `n` smaller iterables.

    :param iterable:
    :param n:
    :return:

    Example:
    >>> tuple(map(tuple, distribute([1, 2, 3, 4, 5], 3)))
    ((1, 4), (2, 5), (3,))
    '''
    copies = itertools_tee(iterable, n)
    return tuple(
        itertools_islice(copy, idx, None, n)
        for idx, copy in builtin_enumerate(copies)
    )


@export_from_module
def partition(iterable, predicate):
    '''
    Splits items from `iterable` into two iterators w/ `predicate`-positive and `predicate`-negative elements.

    :param iterable:
    :param predicate:
    :return:

    Example:
    >>> tuple(map(tuple, partition('AbC', str.isupper)))
    (('A', 'C'), ('b',))
    '''
    copy1, copy2 = itertools_tee(iterable, 2)
    positive = builtin_filter(predicate, copy1)
    negative = itertools_filterfalse(predicate, copy2)
    return positive, negative


@export_from_module
def split_after(iterable, predicate):
    '''
    Splits `iterable` after every `predicate`-positive item into sub-iterators.

    :param iterable:
    :param predicate:
    :return:

    Example:
    >>> tuple(map(''.join, split_after("Ok!Let's go!", lambda c: c == '!')))
    ('Ok!', "Let's go!")
    '''
    spy_it = SpyIterator(iterable)

    def split_chunk_gen(it, pred):
        for item in it:
            if pred(item):
                yield item
                return
            else:
                yield item

    while spy_it.spy().is_ok:
        yield split_chunk_gen(spy_it, predicate)


@export_from_module
def split_at(iterable, predicate):
    '''
    Splits `iterable` on every `predicate`-positive item into sub-iterators. Delimiting items are not included.

    :param iterable:
    :param predicate:
    :return:

    Example:
    >>> tuple(map(tuple, split_at([1, 2, 0, 4, 5, 0], bool)))
    ((1, 2), (4, 5), ())
    '''
    spy_it = SpyIterator(iterable)
    previously_splitted = Flag()

    def split_chunk_gen(it, pred):
        for item in it:
            if pred(item):
                previously_splitted.set()
                return
            else:
                yield item

    while spy_it.spy().is_ok or previously_splitted:
        previously_splitted.clear()
        yield split_chunk_gen(spy_it, predicate)


@export_from_module
def split_before(iterable, predicate):
    '''
    Splits `iterable` before every `predicate`-positive item into sub-iterators.

    :param iterable:
    :param predicate:
    :return:

    Example:
    >>> tuple(map(''.join, split_before("Ok!Let's go!", str.isupper)))
    ('Ok!', "Let's go!")
    '''
    spy_it = SpyIterator(iterable)

    def split_chunk_gen(spy_it, pred):
        ok, item = spy_it.spy()
        if pred(item):
            next(spy_it) # skip first if `pred`-positive
            yield item
            ok, item = spy_it.spy()

        while ok and not pred(item):
            next(spy_it)  # consume one
            yield item
            ok, item = spy_it.spy()

    while spy_it.spy().is_ok:
        yield split_chunk_gen(spy_it, predicate)


@export_from_module
def unzip(iterable, arity=2):
    '''
    Produces `arity`-count of iterators from `iterable`. i-th iterator yields every i-th element from `arity`-length item.

    :param iterable:
    :param arity:
    :return:

    Example:
    >>> tuple(map(tuple, unzip([(1, 2, 3), (4, 5, 6)], arity=3)))
    ((1, 4), (2, 5), (3, 6))
    '''
    if not isinstance(arity, int) or arity < 2:
        raise TypeError('`arity` must be integer greater or equal to 2')
    if arity == 2:
        copy1, copy2 = itertools_tee(iterable, 2)
        first_flow = (first for first, _ in copy1)
        second_flow = (second for _, second in copy2)
        return first_flow, second_flow
    else:
        return tuple(
            (builtin_map(operator_itemgetter(idx), copy)
             for idx, copy in builtin_enumerate(itertools_tee(iterable, arity)))
        )
