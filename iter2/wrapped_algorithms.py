from functools import wraps

from .iterators.iterator2 import Iterator2

from .algorithms import extra
from .algorithms import merging


def wraps_algo(func):
    def wraps_algo_func(dummy):
        func.__doc__ = func.__doc__ + \
            '\n---\nNote: This version wraps result into `Iterator2`'
        @wraps(func)
        def wrapper(*args, **kwargs):
            return Iterator2(func(*args, **kwargs))
        return wrapper
    return wraps_algo_func


@wraps_algo(extra.cartesian_product)
def castesian_product(*iterables, repeat=1):
    pass


@wraps_algo(extra.sort_together)
def sort_together(*iterables, key_list=(0,), key_func=None, reverse=False):
    pass


@wraps_algo(extra.unique_to_each)
def unique_to_each(*iterables):
    pass


@wraps_algo(merging.chain)
def chain(*iterables):
    pass


@wraps_algo(merging.chain_from_iterable)
def chain_from_iterable(iterable):
    pass


@wraps_algo(merging.interleave)
def interleave(*iterables):
    pass


@wraps_algo(merging.interleave_shortest)
def interleave_shortest(*iterables):
    pass


@wraps_algo(merging.roundrobin)
def roundrobin(*iterables):
    pass


@wraps_algo(merging.zip)
def zip(*iterables):
    pass


@wraps_algo(merging.zip_longest)
def zip_longest(*iterables, fillvalue=None):
    pass


@wraps_algo(merging.zip_offset)
def zip_offset(*iterables, offsets, fillvalue=None, longest=None):
    pass

