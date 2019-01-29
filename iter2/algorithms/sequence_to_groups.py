import itertools
import operator
import collections

from . import merging
from iter2.utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Aliases
builtin_enumerate = enumerate
builtin_filter = filter
builtin_map = map
builtin_zip = zip

itertools_groupby = itertools.groupby
itertools_islice = itertools.islice
itertools_permutations = itertools.permutations
itertools_tee = itertools.tee
itertools_zip_longest = itertools.zip_longest

collections_deque = collections.deque
operator_itemgetter = operator.itemgetter

merging_zip_offset = merging.zip_offset


@export_from_module
def chunks(iterable, size, *, allow_partial=False):
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
        yield from builtin_zip(*it_copies)
    else:
        it = iter(iterable)
        next_diff_piece = tuple(itertools_islice(it, size))
        while len(next_diff_piece) == size:
            yield next_diff_piece
            next_diff_piece = tuple(itertools_islice(it, size))
        if len(next_diff_piece) > 0:
            yield next_diff_piece


@export_from_module
def chunks_with_padding(iterable, size, *, fillvalue=None):
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
    return itertools_zip_longest(*it_copies, fillvalue=fillvalue)


@export_from_module
def consecutive_groups(iterable, *, ordering=None):
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
    if ordering is None:
        key = lambda idx, item: idx - item
    else:
        key = lambda idx, item: idx - ordering(item)
    return (
        builtin_map(operator_itemgetter(1), sub_iter)
        for _, sub_iter in itertools_groupby(builtin_enumerate(iterable), key=(lambda item: key(*item)))
    )


@export_from_module
def group_by(iterable, *, key=None):
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
    return itertools_groupby(iterable, key=key)



@export_from_module
def pairwise(iterable):
    '''
    Groups items in overlapping pairs from the original.

    :param iterable:
    :return:

    Example:
    >>> tuple(pairwise([1, 2, 3]))
    ((1, 2), (2, 3))
    '''
    copy1, copy2 = itertools_tee(iterable, 2)
    next(copy2, None)
    return builtin_zip(copy1, copy2)


@export_from_module
def permutations(iterable, length=None):
    '''
    Return successive `length`-permutations of items in the `iterable`.

    :param iterable:
    :param length:
    :return:

    Example:
    >>> tuple(permutations([0, 1, 2], length=2))
    ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))
    '''
    return itertools_permutations(iterable, r=length)


@export_from_module
def process_in_groups(iterable, *, key=None, transformation=None, aggregator=None):
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
    result = itertools_groupby(iterable, key=key)
    if transformation is not None:
        result = (
            (val, builtin_map(transformation, sub_iter))
            for val, sub_iter in result
        )
    if aggregator is not None:
        result = (
            (val, aggregator(sub_iter))
            for val, sub_iter in result
        )
    return result


@export_from_module
def sliding_window(iterable, *, size=1, step=1, allow_partial=False):
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
        yield from chunks(iterable, size, allow_partial=allow_partial)
        return  # done

    # TODO: think about optimizing iteration in chunks

    it = iter(iterable)
    first_piece = tuple(itertools_islice(it, size))
    if len(first_piece) != size and not allow_partial:
        return  # not enough elements
    yield first_piece

    if step < size:
        dq = collections_deque(first_piece, maxlen=size)
        next_diff_piece = tuple(itertools_islice(it, step))
        while len(next_diff_piece) == step:
            dq.extend(next_diff_piece)
            yield tuple(dq)
            next_diff_piece = tuple(itertools_islice(it, step))
        if allow_partial and len(next_diff_piece) > 0:
            yield next_diff_piece
    else:  # step > size
        next_diff_piece = tuple(itertools_islice(it, step))
        while len(next_diff_piece) == step:
            yield next_diff_piece[-size:]
            next_diff_piece = tuple(itertools_islice(it, step))
        if allow_partial and len(next_diff_piece) > 0:
            idx_of_start = len(next_diff_piece) - (step - size)
            yield next_diff_piece[idx_of_start:]


@export_from_module
def stagger(iterable, *, offsets=(-1, 0, 1), fillvalue=None, longest=False):
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
    copies = itertools_tee(iterable, len(offsets))
    return merging_zip_offset(*copies, offsets=offsets, fillvalue=fillvalue, longest=longest)

