import itertools
import collections
import contextlib
import operator

from . import sequence_to_groups

from iter2.utils import alias_for, define_module_exporter


export_from_module, __all__ = define_module_exporter()


# Aliases
builtin_enumerate = enumerate
builtin_filter = filter
builtin_map = map
builtin_slice = slice
builtin_zip = zip

itertools_accumulate = itertools.accumulate
itertools_chain = itertools.chain
itertools_chain_from_iterable = itertools.chain.from_iterable
itertools_cycle = itertools.cycle
itertools_dropwhile = itertools.dropwhile
itertools_filterfalse = itertools.filterfalse
itertools_groupby = itertools.groupby
itertools_islice = itertools.islice
itertools_starmap = itertools.starmap
itertools_takewhile = itertools.takewhile
itertools_tee = itertools.tee

collections_deque = collections.deque
contextlib_suppress = contextlib.suppress

s2g_chunks = sequence_to_groups.chunks


@export_from_module
def accumulate(iterable, func=None, *, initial=None):
    '''
    Return series of accumulated results of binary `func`.
    If `initial` is present then it will be used as first accumulated value.

    :param iterable:
    :param func:
    :param initial:
    :return:

    Example:
    >>> tuple(accumulate([1, 2, 3]))
    (1, 3, 6)
    >>> tuple(accumulate([1, 2, 3], lambda x, y: x * y))
    (1, 2, 6)
    '''
    if initial is not None:
        it = itertools_chain((initial,), iterable)
    else:
        it = iterable
    if func is None:
        return itertools_accumulate(it)
    else:
        return itertools_accumulate(it, func)


@export_from_module
def add_side_effect(iterable, func, *, chunk_size=None, before=None, after=None):
    '''
    Returns new iterator that calls `func` w/ every item from `iterable` as first argument but yields original items.
    If `chunk_size` is set to value bigger than 1 then calls `func` w/ every chunk of `chunk_size` as first argument.
    If `before` is set then calls `before` in the beginning of iteration.
    If `after` is set then calls `after` in the end of iteration.

    :param iterable:
    :param func:
    :param chunk_size:
    :param before:
    :param after:
    :return:

    Example:
    >>> tuple(add_side_effect(['Julia', 'Angelina', 'Jessica'], lambda w: print('  %s' % w), before=lambda: 'My list:', after=print))
    My list:
      Julia
      Angelina
      Jessica

    ('Julia', 'Angelina', 'Jessica')
    >>> tuple(add_side_effect(range(10), lambda ch: print('Processed: %s' % repr(ch)), chunk_size=4))
    Processed: (0, 1, 2, 3)
    Processed: (4, 5, 6, 7)
    Processed: (8, 9)
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    '''
    try:
        if before is not None:
            before()
        if chunk_size is None or chunk_size == 1:
            for item in iterable:
                func(item)
                yield item
        else:
            for chunk in s2g_chunks(iterable, chunk_size, allow_partial=True):
                func(chunk)
                yield from chunk
    finally:
        if after is not None:
            after()


@export_from_module
def consume(iterable, number=None):
    '''
    Consumes `number` of items from `iterable`. If `number` is not present then whole iterable is consumed.

    :param iterable:
    :param number:
    :return:

    Example:
    >>> tuple(consume(range(10)))
    ()
    >>> tuple(consume(range(10), 8))
    (8, 9)
    '''
    iterable = iter(iterable)  # it can look like iterable but it's not (e.g. range(10))
    if number is None:
        collections_deque(iterable, maxlen=0)  # fastest full consume ever
    else:
        next(itertools_islice(iterable, number, number), None)
    return iterable


@export_from_module
def cycle(iterable, *, number=None):
    '''
    Returns iterator that yields items from `iterable` in cycle `number` times.
    If `number` is not present then cycle is infinite.

    :param iterable:
    :param number:
    :return:

    Example:
    >>> tuple(cycle([0, 1], number=2))
    (0, 1, 0, 1)
    '''
    if number is None:
        return itertools_cycle(iterable)
    else:
        # TODO: think about (micro)optimization
        return itertools_chain_from_iterable(itertools_tee(iterable, number))


@export_from_module
def dedup(iterable):
    '''
    Reduces consecutive repetitions of items in `iterable` to one. Doesn't make items unique in sequence.

    :param iterable:
    :return:

    Example:
    >>> ''.join(dedup('011011110011'))
    '010101'
    '''
    for val, sub_iter in itertools_groupby(iterable):
        yield val
        consume(sub_iter)


@export_from_module
def difference(iterable, func=operator.sub, *, initial=None):
    '''
    By default, compute the first difference of `iterable` using `operator.sub`. This is the opposite of `accumulate`’s default behavior.
    By default `func` is operator.sub(), but other functions can be specified. They will be applied as follows:
        A, B, C, D, ... --> A, func(B, A), func(C, B), func(D, C), ...
    If `initial` is present then it will be used as first value.

    :param iterable:
    :param func:
    :param initial:
    :return:

    Example:
    >>> tuple(difference([1, 3, 6]))
    (1, 2, 3)

    '''
    if initial is not None:
        it = itertools_chain((initial,), iterable)
    else:
        it = iterable
    a, b = itertools_tee(it)
    try:
        item = next(b)
        return itertools_chain((item,), builtin_map(lambda x: func(x[1], x[0]), builtin_zip(a, b)))
    except StopIteration:
        return iter(())


@export_from_module
def drop(iterator, number=1):
    '''
    Skips `number` of items from `iterator`.

    :param iterator:
    :param number:
    :return:

    Example:
    >>> tuple(drop(range(10), 8))
    (8, 9)
    '''
    return itertools_islice(iterator, number, None)


@export_from_module
def drop_while(iterator, predicate):
    '''
    Skips items from `iterator` while `predicate` is true.

    :param iterator:
    :param predicate:
    :return:

    Example:
    >>> tuple(drop_while('aaaaAAAA'), str.islower)
    ('A', 'A', 'A', 'A')
    '''
    return itertools_dropwhile(predicate, iterator)


@export_from_module
def enumerate(iterable, *, count_from=0):
    '''
    Returns iterator that yields pairs (index, item) where index starts from `count_from`.

    :param iterable:
    :param count_from:
    :return:

    Example:
    >>> tuple(enumerate('ab'))
    ((0, 'a'), (1, 'b'))
    '''
    return builtin_enumerate(iterable, count_from)


@export_from_module
def filter(iterable, predicate, *, inverse=False):
    '''
    Returns iterator that yields `predicate`-positive items from `iterable`.
    If `inverse` is true then yields `predicate`-negative items.

    :param iterable:
    :param predicate:
    :param inverse:
    :return:

    Example:
    >>> tuple(filter('aAaA', str.isupper))
    ('A', 'A')
    >>> tuple(filter('aAaA', str.isupper, inverse=True))
    ('a', 'a')
    '''
    if inverse:
        func = itertools_filterfalse
    else:
        func = builtin_filter
    return func(predicate, iterable)


@export_from_module
def filter_none(iterable):
    '''
    Filters builtin `None` values from `iterable`.

    :param iterable:
    :return:

    Example:
    >>> tuple(filter_none([1, None, 2, None]))
    (1, 2)
    '''
    return (
        val
        for val in iterable
        if val is not None
    )


@export_from_module
def flatmap(iterable, func):
    '''
    Assuming `func` produces iterables, applies `func` to each item in `iterable` and yields new items one-by-one from new iterables.
    Is equivalent to flatten(map(iterable, func)).

    :param iterable:
    :param func:
    :return:

    Example:
    >>> tuple(flatmap(['one two', 'three four', 'five'], str.split))
    ('one', 'two', 'three', 'four', 'five')
    '''
    return itertools_chain.from_iterable(builtin_map(func, iterable))


@export_from_module
def flatten(iterable):
    '''
    Assuming iterables consists from another iterables, yields items from "sub-iterables" one-by-one.

    :param iterable:
    :return:

    Example:
    >>> tuple(flatten(((1, 2), (3,))))
    (1, 2, 3)
    '''
    return itertools_chain.from_iterable(iterable)


@export_from_module
def intersperse(iterable, item):
    '''
    Returns iterator where `item` is placed between original items.

    :param iterable:
    :param item:
    :return:

    Example:
    >>> tuple(intersperse([1, 2, 3], 0))
    (1, 0, 2, 0, 3)
    '''
    # TODO: think about better solution
    it = iter(iterable)
    with contextlib_suppress(StopIteration):
        yield next(it)
        for elem in it:
            yield item
            yield elem


@export_from_module
def map(iterable, func):
    '''
    Returns iterator where `func` is applied to every item in `iterable`.

    :param iterable:
    :param func:
    :return:

    Example:
    >>> tuple(map('abc', str.upper))
    ('A', 'B', 'C')
    '''
    return builtin_map(func, iterable)


@export_from_module
@alias_for(drop)
def skip(iterable, number=1):
    pass


@export_from_module
@alias_for(drop_while)
def skip_while(iterable, predicate):
    pass


@export_from_module
@alias_for(itertools_islice)
def slice(iterable, *args):
    # TODO: make it work for all variants of `start`, `stop`, `step`, e.g. negative ones. See more-itertools.
    # Note: don't forget to remove @alias_for
    pass


@export_from_module
def starmap(iterable, func):
    '''
    Returns iterable where `func` is applied to every item in `iterable`, assuming that items are iterables with common length and `func`
    is a function of that length arguments.

    :param iterable:
    :param func:
    :return:

    Example:
    >>> tuple(starmap(('ab', 'ac', 'za'), lambda f, s: f > s))
    (False, False, True)
    '''
    return itertools_starmap(func, iterable)


@export_from_module
def step(iterable, k=1):
    '''
    Returns an iterator that yields every `k`th item from `iterable`.

    :param iterable:
    :param k:
    :return:

    Example:
    >>> tuple(step('abcdef', 3))
    ('a', 'd')
    '''
    return itertools_islice(iterable, None, None, k)


@export_from_module
def take(iterable, number=1):
    '''
    Returns an iterable that yields at *most* `number` first items from `iterable`.
    "Taken" items are not consumed from original iterable after function call.

    :param iterable:
    :param number:
    :return:

    Example:
    >>> tuple(take(range(100000000), 3))
    (0, 1, 2)
    '''
    return itertools_islice(iterable, number)


@export_from_module
def take_now(iterable, number=1):
    '''
    Returns a tuple with at *most* `number` first items from `iterable`.

    :param iterable:
    :param number:
    :return:

    Example:
    >>> take_now(range(1000000000), 3)
    (0, 1, 2)
    '''
    return tuple(itertools_islice(iterable, number))


@export_from_module
def take_last(iterable, number=1):
    '''
    Returns a tuple with at *most* `number` last items from `iterable`.

    :param iterator:
    :param number:
    :return:

    Example:
    >>> take_last('abcdef', 3)
    ('d', 'e', 'f')
    '''
    return tuple(collections_deque(iterable, maxlen=number))


@export_from_module
def take_while(iterable, predicate):
    '''
    Returns an iterable that yields original items while `predicate` is True. "Taken" items are not consumed from original iterable
    after function call.
    Note: first `predicate`-negative item will be consumed (see Example section).

    :param iterator:
    :param predicate:
    :return:

    Example:
    >>> it = iter('abcDef'); tuple(take_while(it, str.islower)), tuple(it)
    (('a', 'b', 'c'), ('e', 'f'))
    '''
    return itertools_takewhile(predicate, iterable)

