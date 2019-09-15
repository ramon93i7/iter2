import itertools
import operator

from iter2.iterators.spy_iterator import SpyIterator
from iter2.utils import define_module_exporter, Flag


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin__enumerate = enumerate
builtin__filter = filter
builtin__map = map

itertools__filterfalse = itertools.filterfalse
itertools__islice = itertools.islice
itertools__tee = itertools.tee

operator__itemgetter = operator.itemgetter


UNDEFINED = object()


@export_from_module
def distribute(iterable, n, *, collect_to=tuple, wrap_into=UNDEFINED):
    '''
    Distributes items from `iterable` among `n` smaller iterables.

    :param iterable:
    :param n:
    :return:

    Example:
    >>> tuple(map(tuple, distribute([1, 2, 3, 4, 5], 3)))
    ((1, 4), (2, 5), (3,))
    '''
    copies = itertools__tee(iterable, n)
    result = (
        itertools__islice(copy, idx, None, n)
        for idx, copy in builtin__enumerate(copies)
    )
    if wrap_into is not UNDEFINED:
        result = builtin__map(wrap_into, result)
    return collect_to(result)


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
    copy1, copy2 = itertools__tee(iterable, 2)
    positive = builtin__filter(predicate, copy1)
    negative = itertools__filterfalse(predicate, copy2)
    return positive, negative


@export_from_module
def split_after(iterable, predicate, *, wrap_into=UNDEFINED):
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

    def split_chunk_cycle(spy_it, predicate):
        while spy_it.spy().is_ok:
            yield split_chunk_gen(spy_it, predicate)

    result = split_chunk_cycle(spy_it, predicate)
    if wrap_into is not UNDEFINED:
        result = builtin__map(wrap_into, result)
    return result


@export_from_module
def split_at(iterable, predicate, *, wrap_into=UNDEFINED):
    '''
    Splits `iterable` on every `predicate`-positive item into sub-iterators. Delimiting items are not included.

    :param iterable:
    :param predicate:
    :return:

    Example:
    >>> tuple(map(tuple, split_at([1, 2, 0, 4, 5, 0], bool)))
    ((1, 2), (4, 5), ())
    '''

    # TODO: there is a bug w/ non sequential access to chunks - general problem "Dependent Iterators Problem"

    def split_chunk_gen(it, pred, previously_splitted):
        for item in it:
            if pred(item):
                previously_splitted.set()
                return
            else:
                yield item

    def split_chunk_cycle(iterable, predicate):
        spy_it = SpyIterator(iterable)
        previously_splitted = Flag()
        while spy_it.spy().is_ok or previously_splitted:
            previously_splitted.clear()
            yield split_chunk_gen(spy_it, predicate, previously_splitted)

    result = split_chunk_cycle(iterable, predicate)
    if wrap_into is not UNDEFINED:
        result = builtin__map(wrap_into, result)
    return result


@export_from_module
def split_before(iterable, predicate, *, wrap_into=UNDEFINED):
    '''
    Splits `iterable` before every `predicate`-positive item into sub-iterators.

    :param iterable:
    :param predicate:
    :return:

    Example:
    >>> tuple(map(''.join, split_before("Ok!Let's go!", str.isupper)))
    ('Ok!', "Let's go!")
    '''
    # TODO: "Dependent Iterators Problem"
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

    def split_chunk_cycle(iterable, predicate):
        spy_it = SpyIterator(iterable)
        while spy_it.spy().is_ok:
            yield split_chunk_gen(spy_it, predicate)

    result = split_chunk_cycle(iterable, predicate)
    if wrap_into is not UNDEFINED:
        result = builtin__map(wrap_into, result)
    return result


@export_from_module
def unzip(iterable, arity=2, collect_to=tuple, wrap_into=UNDEFINED):
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
    result = (
        (builtin__map(operator__itemgetter(idx), copy)
         for idx, copy in builtin__enumerate(itertools__tee(iterable, arity)))
    )
    if wrap_into is not UNDEFINED:
        result = builtin__map(wrap_into, result)
    return collect_to(result)

