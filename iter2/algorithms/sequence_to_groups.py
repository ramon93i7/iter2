import itertools
import operator
import collections

from . import base
from . import merging
from iter2.utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin__enumerate = enumerate
builtin__filter = filter
builtin__map = map
builtin__zip = zip

itertools__groupby = itertools.groupby
itertools__islice = itertools.islice
itertools__permutations = itertools.permutations
itertools__tee = itertools.tee
itertools__zip_longest = itertools.zip_longest

collections__deque = collections.deque
operator__itemgetter = operator.itemgetter

base__take_now = base.take_now
merging__zip_offset = merging.zip_offset


UNDEFINED = object()


@export_from_module
def chunks(iterable, size, *, allow_partial=False, collect_to=tuple):
    '''
    Groups items in chunks of size `size`. If `allow_partial` is True last chunk may be incomplete.

    :param iterable:
    :param size:  length of chunk
    :param allow_partial:
    :return:  tuples of size `size`

    Example:
    >>> tuple(chunks([1, 2, 3, 4], 2))
    ((1, 2), (3, 4))
    >>> tuple(chunks([1, 2, 3], 2, allow_partial=True))
    ((1, 2), (3,))
    '''
    if allow_partial is False:
        it_copies = (iter(iterable),) * size
        chunks_stream = builtin__zip(*it_copies)
        if collect_to is not tuple:
            chunks_stream = builtin__map(collect_to, chunks_stream)
        yield from chunks_stream
    else:
        it = iter(iterable)
        next_diff_piece = base__take_now(it, size, collect_to)
        while len(next_diff_piece) == size:
            yield next_diff_piece
            next_diff_piece = base__take_now(it, size, collect_to)
        if len(next_diff_piece) > 0:
            yield next_diff_piece


@export_from_module
def chunks_with_padding(iterable, size, *, fillvalue=None, collect_to=tuple):
    '''
    Groups items in chunks of size `size`. Fills incomplete chunk with `fillvalue`.

    :param iterable:
    :param size:
    :param fillvalue:
    :return:  tuples of size `size`

    Example:
    >>> tuple(chunks_with_padding([1, 2, 3, 4], 2))
    ((1, 2), (3, 4))
    >>> tuple(chunks_with_padding([1, 2, 3], 2, fillvalue=100500))
    ((1, 2), (3, 100500))
    '''
    it_copies = (iter(iterable),) * size
    chunks_stream = itertools__zip_longest(*it_copies, fillvalue=fillvalue)
    if collect_to is not tuple:
        chunks_stream = builtin__map(collect_to, chunks_stream)
    return chunks_stream


@export_from_module
def consecutive_groups(iterable, *, ordering=UNDEFINED, wrap_into=UNDEFINED):
    '''
    Groups items which are consecutive due to `ordering`. If `ordering` is None then it is assumed that items are integers.

    :param iterable:
    :param ordering:
    :return: tuples of consecutive groups

    Example:
    >>> tuple(consecutive_groups([1, 2, 10, 11, 100, 101]))
    ((1, 2), (10, 11), (100, 101))
    >>> tuple(consecutive_groups('abcBCDcde', ordering=ord))
    (('a', 'b', 'c'), ('B', 'C', 'D'), ('c', 'd', 'e'))
    '''
    if ordering is UNDEFINED:
        key = lambda idx, item: idx - item  # TODO: precalc
    else:
        key = lambda idx, item: idx - ordering(item)
    result_groups_streams = (
        builtin__map(operator__itemgetter(1), sub_iter)
        for _, sub_iter in itertools__groupby(builtin__enumerate(iterable), key=(lambda item: key(*item)))
    )
    if wrap_into is not UNDEFINED:
        result_groups_streams = builtin__map(wrap_into, result_groups_streams)
    return result_groups_streams


@export_from_module
def group_by(iterable, *, key=None, wrap_into=UNDEFINED):
    '''
    Groups items in consecutive keys and groups from the `iterable`.
    If `key` function is not specified or is None, the element itself is a key for grouping.

    :param iterable:
    :param key:
    :return:

    Example:
    >>> for k, group in group_by([1, 2, 2, 3, 3, 3], key=lambda x: x % 2):
    ...     print((k, tuple(group)))
    (1, (1,))
    (0, (2, 2))
    (1, (3, 3, 3))
    '''
    group_stream = itertools__groupby(iterable, key=key)
    if wrap_into is not UNDEFINED:
        group_stream = (
            (item, wrap_into(sub_iter))
            for item, sub_iter in group_stream
        )
    return group_stream



@export_from_module
def pairwise(iterable, *, collect_to=tuple):
    '''
    Groups items in overlapping pairs from the original.

    :param iterable:
    :return:

    Example:
    >>> tuple(pairwise([1, 2, 3]))
    ((1, 2), (2, 3))
    '''
    copy1, copy2 = itertools__tee(iterable, 2)
    next(copy2, None)
    pairs = builtin__zip(copy1, copy2)
    if collect_to is not tuple:
        pairs = builtin__map(collect_to, pairs)
    return pairs


@export_from_module
def permutations(iterable, length=None, *, collect_to=tuple):
    '''
    Return successive `length`-permutations of items in the `iterable`.

    :param iterable:
    :param length:
    :return:

    Example:
    >>> tuple(permutations([0, 1, 2], length=2))
    ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))
    '''
    records = itertools__permutations(iterable, r=length)
    if collect_to is not tuple:
        records = builtin__map(collect_to, records)
    return records


@export_from_module
def process_in_groups(iterable, *, key=None, transformation=UNDEFINED, aggregator=UNDEFINED):
    '''
    Groups items in consecutive keys and groups from the `iterable`.
    If `key` function is not specified or is None, the element itself is a key for grouping.
    If `transformation` is specified then it will be applied to each item.
    If `aggregator` is specified then it will be applied to each group.

    :param iterable:
    :param key:
    :param transformation:
    :param aggregator:
    :return:

    Example:
    >>> for k, group in process_in_groups([1, 2, 2, 3, 3, 3], key=lambda x: x % 2):
    ...     print((k, tuple(group)))
    (1, (1,))
    (0, (2, 2))
    (1, (3, 3, 3))
    >>> for k, group in process_in_groups([1, 2, 2, 3, 3, 3], transformation=lambda x: x % 2):
    ...     print((k, tuple(group)))
    (1, (1,))
    (2, (0, 0))
    (3, (1, 1, 1))
    >>> for k, val in process_in_groups([1, 2, 2, 3, 3, 3], aggregator=sum):
    ...     print((k, val))
    (1, 1)
    (2, 4)
    (3, 9)
    '''
    result = itertools__groupby(iterable, key=key)
    if transformation is not UNDEFINED:
        result = (
            (val, builtin__map(transformation, sub_iter))
            for val, sub_iter in result
        )
    if aggregator is not UNDEFINED:
        result = (
            (val, aggregator(sub_iter))
            for val, sub_iter in result
        )
    return result


@export_from_module
def sliding_window(iterable, *, size=1, step=1, allow_partial=False, collect_to=tuple):
    '''
    Sliding window (#docs_in_pictures, size=5, step=4)
    iterable:   a b c d e f g h i j k
               [         ] <- "window" (step 0)
               <- size ->
    res[0]:    (a,b,c,d,e)
    iterable:   a b c d e f g h i j k
                       [         ] <- "window" (step 1)
               <-step->
    res[1]:    (e, f, g, h, i)
    iterable:   a b c d e f g h i j k
                               [         ] <- "window" (step 2)
    res[2]:    (i, j, k)   # if `allow_partial` is True

    :param iterable:
    :param step:
    :param size:
    :param allow_partial:
    :return:
    '''
    if step == size:
        return chunks(iterable, size, allow_partial=allow_partial, collect_to=collect_to)

    # TODO: think about optimizing iteration in chunks

    it = iter(iterable)
    first_piece = base__take_now(it, size)
    if len(first_piece) != size and not allow_partial:
        return  # not enough elements
    yield first_piece

    if step < size:
        dq = collections__deque(first_piece, maxlen=size)
        next_diff_piece = base__take_now(it, step)
        while len(next_diff_piece) == step:
            dq.extend(next_diff_piece)
            yield collect_to(dq)
            next_diff_piece = base__take_now(it, step)
        if allow_partial and len(next_diff_piece) > 0:
            yield collect_to(next_diff_piece)
    else:  # step > size
        next_diff_piece = base__take_now(it, step)
        while len(next_diff_piece) == step:
            yield collect_to(next_diff_piece[-size:])
            next_diff_piece = base__take_now(it, step)
        if allow_partial and len(next_diff_piece) > 0:
            idx_of_start = len(next_diff_piece) - (step - size)
            yield collect_to(next_diff_piece[idx_of_start:])


@export_from_module
def stagger(iterable, *, offsets=(-1, 0, 1), fillvalue=None, longest=False, collect_to=tuple):
    '''
    Yields tuples whose elements are offset from iterable.
    The amount by which the i-th item in each tuple is offset is given by the i-th item in `offsets`.
    >>> tuple(stagger([0, 1, 2, 3]))
    ((None, 0, 1), (0, 1, 2), (1, 2, 3))
    >>> tuple(stagger(range(8), offsets=(0, 2, 4)))
    ((0, 2, 4), (1, 3, 5), (2, 4, 6), (3, 5, 7))

    By default, the sequence will end when the final element of a tuple is the last item in the `iterable`.
    To continue until the first element of a tuple is the last item in the iterable, set `longest` to True:
    >>> tuple(stagger([0, 1, 2, 3], longest=True))
    ((None, 0, 1), (0, 1, 2), (1, 2, 3), (2, 3, None), (3, None, None))

    By default, None will be used to replace offsets beyond the end of the sequence.
    Specify `fillvalue` to use some other value.

    :param iterable:
    :param offsets:
    :param fillvalue:
    :param longest:
    :return:
    '''
    copies = itertools__tee(iterable, len(offsets))
    return merging__zip_offset(*copies, offsets=offsets, fillvalue=fillvalue, longest=longest, collect_to=collect_to)

