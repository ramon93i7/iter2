import itertools
from functools import wraps

from iter2 import algorithms
from iter2.option import Some2, None2
from iter2.iterators.spy_iterator import SpyIterator

from iter2.utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup export


# Shortcuts
algorithms_take = algorithms.sequence_to_sequence.take
algorithms_take_now = algorithms.sequence_to_sequence.take_now
algorithms_take_last = algorithms.sequence_to_sequence.take_last
algorithms_take_while = algorithms.sequence_to_sequence.take_while
algorithms_group_by = algorithms.sequence_to_groups.group_by
algorithms_process_in_groups = algorithms.sequence_to_groups.process_in_groups
algorithms_position = algorithms.searching.position
algorithms_chain_from_iterable = algorithms.merging.chain_from_iterable

itertools_chain = itertools.chain
itertools_islice = itertools.islice
itertools_starmap = itertools.starmap
itertools_tee = itertools.tee


class InvalidIteratorClass(object):
    def __iter__(self):
        raise ValueError('Iterating invalidated iterator (probably original was moved).')

    def __next__(self):
        raise ValueError('Iterating invalidated iterator (probably original was moved).')


InvalidIterator = InvalidIteratorClass()


def merge_docs(method, algorithm_function):
    header = method.__doc__ or 'Derived from function `{fname}`'.format(fname=algorithm_function.__qualname__)
    return '\n---\n'.join([header, algorithm_function.__doc__])


def derived_from(algorithm_function, *, wrap_into_iterator=True):
    def derive_from_algo_func(method):
        method.__doc__ = merge_docs(method, algorithm_function)
        if wrap_into_iterator:
            @wraps(method)
            def wrapper(self, *args, **kwargs):
                return Iterator2(algorithm_function(self.raw(), *args, **kwargs))
        else:
            @wraps(method)
            def wrapper(self, *args, **kwargs):
                return algorithm_function(self.raw(), *args, **kwargs)
        return wrapper
    return derive_from_algo_func


def based_on(algorithm_function):
    def base_on_algo_func(method):
        method.__doc__ = merge_docs(method, algorithm_function)
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            self._iterator = algorithm_function(self._iterator, *args, **kwargs)  # patches inner iterator with algo
            return method(self, *args, **kwargs)
        return wrapper
    return base_on_algo_func


def with_rich_subiterators(*, in_tuple=False):
    def _with_rich_subiterators(method):
        if in_tuple:
            @wraps(method)
            def wrapper(self, *args, **kwargs):
                return tuple(map(Iterator2, self.raw()))
        else:
            @wraps(method)
            def wrapper(self, *args, **kwargs):
                return Iterator2(map(Iterator2, self.raw()))
        return wrapper
    return _with_rich_subiterators


def tuple_wise(func):
    return (lambda item: func(*item))

def tuple_wise_version_of(base_method):
    def tuple_wise_version_of_base_method(method):
        method.__doc__ = '\n'.join([f'Tuple wise option of `{base_method.__name__}`', '---', base_method.__doc__ or ''])
        @wraps(method)
        def wrapper(self, func, *args, **kwargs):
            adapter_func = tuple_wise(func)
            return base_method(self, adapter_func, *args, **kwargs)
        return wrapper
    return tuple_wise_version_of_base_method


@export_from_module
class Iterator2:
    __slots__ = ('_iterator',)

    def __init__(self, *args):
        self._iterator = iter(*args)

    def __repr__(self):
        return '{class_name}<{it_id}>'.format(
            class_name=self.__class__.__name__,
            it_id=hex(id(self))
        )

    # ====================
    # `iterator` behaviour
    # ====================
    def __iter__(self):
        return self  # Do not expose internals.

    def __next__(self):
        return next(self._iterator)  # Proxing next-protocol.

    def next(self):
        try:
            return Some2(next(self._iterator))
        except StopIteration:
            return None2

    def raw(self):
        '''
        Returns inner raw iterator and makes self invalid.

        :return:
        '''
        self._iterator, it = InvalidIterator, self._iterator  # move semantics
        return it

    def ref(self):
        '''
        Creates a copy-by-reference.
        Warning: Assumed to be used in special cases.

        :return:

        Example:
        >>> it = Iterator2(range(20))
        >>> it.ref().take_now(5)  # new Iterator2 that shares raw iterator w/ `it` and then consumes 5 items
        (0, 1, 2, 3, 4)
        >>> it.ref().take_now(5)  # new Iterator2 that also shares raw iterator w/ `it` and then consumes next 5 items
        (5, 6, 7, 8, 9)
        >>> it.take_now(5) #  `it` consumes 5 items and become invalid, {15, 16, 17, 18, 19} are "lost" here
        (10, 11, 12, 13, 14)
        >>> it.raw() is InvalidIterator
        True
        '''
        return Iterator2(self._iterator)

    # =================================
    # Processing "sequence -> sequence"
    # =================================
    @derived_from(algorithms.sequence_to_sequence.add_side_effect)
    def add_side_effect(self, func, *, chunk_size=None, before=None, after=None):
        pass

    def add_side_effect_t(self, func, *, chunk_size=None, before=None, after=None):
        '''Tuple wise version of `add_side_effect`'''
        adapter_func = tuple_wise(func)
        adapter_before = before and tuple_wise(before)
        adapter_after = after and tuple_wise(after)
        return self.add_side_effect(adapter_func, chunk_size=chunk_size, before=adapter_before, after=adapter_after)

    @derived_from(algorithms.sequence_to_sequence.accumulate)
    def accumulate(self, func=None, *, initial=None):
        pass

    @derived_from(algorithms.sequence_to_sequence.consume)
    def consume(self, number=None):
        pass

    @derived_from(algorithms.sequence_to_sequence.cycle)
    def cycle(self, *, number=None):
        pass

    @derived_from(algorithms.sequence_to_sequence.dedup)
    def dedup(self):
        pass

    @derived_from(algorithms.sequence_to_sequence.difference)
    def difference(self, func=None, *, initial=None):
        pass

    @derived_from(algorithms.sequence_to_sequence.drop)
    def drop(self, number=1):
        pass

    @derived_from(algorithms.sequence_to_sequence.drop_while)
    def drop_while(self, predicate):
        pass

    @tuple_wise_version_of(drop_while)
    def drop_while_t(self, predicate):
        pass

    @derived_from(algorithms.sequence_to_sequence.enumerate)
    def enumerate(self, *, count_from=0):
        pass

    @derived_from(algorithms.sequence_to_sequence.filter)
    def filter(self, predicate, *, inverse=False):
        pass

    @tuple_wise_version_of(filter)
    def filter_t(self, predicate, *, inverse=False):
        pass

    @derived_from(algorithms.sequence_to_sequence.filter_none)
    def filter_builtin_none(self):
        pass

    def filter_none(self):
        '''
        Works with sequences of `Option`s. Unwraps `Some`s and filter `None`s.

        :return: new iterator
        Example:
        >>> tuple(Iterator2([Some2(1), None2, Some2(3)]).filter_none())
        (1, 3)
        '''
        self._iterator = (
            val.unwrap()
            for val in self._iterator
            if val.is_some()
        )
        return self

    @derived_from(algorithms.sequence_to_sequence.flatmap)
    def flatmap(self, func):
        pass

    @tuple_wise_version_of(flatmap)
    def flatmap_t(self, func):
        pass

    @derived_from(algorithms.sequence_to_sequence.flatten)
    def flatten(self):
        pass

    def for_each(self, func):
        '''
        Calls `func` on every item. Returns nothing. Is equivalent to:
            for item in it:
                func(it)

        :param func:
        :return:  nothing

        Example:
        >>> Iterator2([1, 2]).for_each(print)
        1
        2
        '''
        for item in self._iterator:
            func(item)

    def foreach(self, func):
        '''
        Alias for `for_each`.

        :param func:
        :return:  nothing
        '''
        for item in self._iterator:
            func(item)

    @tuple_wise_version_of(foreach)
    def foreach_t(self, func):
        pass

    @derived_from(algorithms.sequence_to_sequence.intersperse)
    def intersperse(self, item):
        pass

    @derived_from(algorithms.sequence_to_sequence.map)
    def map(self, func):
        pass

    @derived_from(algorithms.sequence_to_sequence.starmap)
    def map_t(self, func):
        pass

    @derived_from(algorithms.sequence_to_sequence.skip)
    def skip(self, number=1):
        pass

    @derived_from(algorithms.sequence_to_sequence.skip_while)
    def skip_while(self, predicate):
        pass

    @tuple_wise_version_of(skip_while)
    def skip_while_t(self, predicate):
        pass

    @derived_from(algorithms.sequence_to_sequence.slice)
    def slice(self, *args):
        pass

    @derived_from(algorithms.sequence_to_sequence.starmap)
    def starmap(self, func):
        pass

    @derived_from(algorithms.sequence_to_sequence.step)
    def step(self, k=1):
        pass

    @derived_from(algorithms.sequence_to_sequence.take)
    def take(self, number=1):
        pass

    @derived_from(algorithms.sequence_to_sequence.take_now, wrap_into_iterator=False)
    def take_now(self, number=1):
        pass

    def take_into_option(self, number=1):
        '''
        Returns chunk of *exactly* `number`-items from the beginning of iterator wrapped in `Some2`.
        In case of insufficient iterator returns `None2` and *returns* read items back to iterator.
        Note: If `None2` is returned then iterator is not invalidated!

        :param number:
        :return:

        Example:
        >>> it = Iterator2([1, 2, 3]); (it.take_into_option(4).is_none(), it.take_into_option(2).unwrap())
        (True, (1, 2))
        '''
        taken = self.take_now(number)
        if len(taken) == number:
            return Some2(taken)
        else:
            self._iterator = iter(taken)  # returns back, `taken` contains all items *before* take-call
            return None2

    @derived_from(algorithms.sequence_to_sequence.take_last)
    def take_last(self, number=1):
        pass

    @derived_from(algorithms.sequence_to_sequence.take_last, wrap_into_iterator=False)
    def take_last_now(self, number=1):
        pass

    def take_last_into_option(self, number=1):
        '''
        Returns chunk of *exactly* `number`-items from the end of iterator wrapped in `Some2`.
        In case of insufficient iterator returns `None2` and *returns* read items back to iterator.
        Note: If `None2` is returned then iterator is not invalidated!

        :param number:
        :return:

        Example:
        >>> it = Iterator2([1, 2, 3]); (it.take_into_option(4).is_none(), it.take_into_option(2).unwrap())
        (True, (1, 2))
        '''
        taken = self.take_last_now(number)
        if len(taken) == number:
            return Some2(taken)
        else:
            self._iterator = iter(taken)  # returns back, `taken` contains all items *before* take-call
            return None2

    @derived_from(algorithms.sequence_to_sequence.take_while)
    def take_while(self, predicate):
        # TODO: keep border element
        pass

    @tuple_wise_version_of(take_while)
    def take_while_t(self, predicate):
        pass

    # ===================
    # Checking conditions
    # ===================
    @derived_from(algorithms.predicate_on_sequence.all, wrap_into_iterator=False)
    def all(self, predicate):
        pass

    @tuple_wise_version_of(all)
    def all_t(self, predicate):
        pass

    @derived_from(algorithms.predicate_on_sequence.any, wrap_into_iterator=False)
    def any(self, predicate):
        pass

    @tuple_wise_version_of(any)
    def any_t(self, predicate):
        pass

    @derived_from(algorithms.predicate_on_sequence.none, wrap_into_iterator=False)
    def none(self, predicate):
        pass

    @tuple_wise_version_of(none)
    def none_t(self, predicate):
        pass

    # =============
    # Making groups
    # =============
    @derived_from(algorithms.sequence_to_groups.chunks)
    def chunks(self, size, *, allow_partial=False):
        pass

    @derived_from(algorithms.sequence_to_groups.chunks_with_padding)
    def chunks_with_padding(self, size, *, fillvalue=None):
        pass

    @derived_from(algorithms.sequence_to_groups.consecutive_groups)
    def consecutive_groups(self, *, ordering=None):
        pass

    @based_on(algorithms.sequence_to_groups.group_by)
    def group_by(self, *, key=None):
        return Iterator2((
            (val, Iterator2(sub_iter))
            for val, sub_iter in self.raw()
        ))

    def group_by_t(self, *, key=None):
        '''Tuple-wise version of `group_by`'''
        adapter_key = key and tuple_wise(key)
        return self.group_by(key=adapter_key)

    @derived_from(algorithms.sequence_to_groups.pairwise)
    def pairwise(self):
        pass

    @based_on(algorithms.sequence_to_groups.process_in_groups)
    def process_in_groups(self, *, key=None, transformation=None, aggregator=lambda it: Iterator2(it)):
        return Iterator2(self.raw())

    def process_in_groups_t(self, *, key=None, transformation=None, aggregator=lambda it: Iterator2(it)):
        '''Tuple-wise version of `process_in_groups`'''
        adapter_key = key and tuple_wise(key)
        adapter_transformation = transformation and tuple_wise(transformation)
        return self.process_in_groups(key=adapter_key, transformation=adapter_transformation, aggregator=aggregator)

    @derived_from(algorithms.sequence_to_groups.permutations)
    def permutations(self, length=None):
        pass

    @derived_from(algorithms.sequence_to_groups.sliding_window)
    def sliding_window(self, *, step=1, size=1, allow_partial=False):
        pass

    @derived_from(algorithms.sequence_to_groups.stagger)
    def stagger(self, *, offsets=(-1, 0, 1), fillvalue=None, longest=False):
        pass

    # ===========
    # Merging
    # ===========

    @derived_from(algorithms.merging.chain)
    def chain(self, *others):
        pass

    def chain_from_iterable(self, others_in_iterable):
        '''
        Returns a new iterable yielding items from base iterator and then from `other_in_iterable`, iterable by iterable.
        This is the same as `chain` but consumes iterables from another iterable.

        :param others_in_iterable:
        :return:  chained iterables as new iterable

        Example:
        >>> Iterator2('ab').chain_from_iterable(['cd', 'ef'])).to_list()
        ['a', 'b', 'c', 'd', 'e', 'f']
        '''
        return Iterator2(itertools_chain(self.raw(), algorithms_chain_from_iterable(others_in_iterable)))


    @derived_from(algorithms.merging.interleave)
    def interleave(self, *others):
        pass

    @derived_from(algorithms.merging.interleave_shortest)
    def interleave_shortest(self, *others):
        pass

    @derived_from(algorithms.merging.prepend)
    def prepend(self, iterable):
        pass

    @derived_from(algorithms.merging.roundrobin)
    def roundrobin(self, *others):
        pass

    @derived_from(algorithms.merging.zip)
    def zip(self, *others):
        pass

    @derived_from(algorithms.merging.zip_longest)
    def zip_longest(self, *others, fillvalue=None):
        pass

    @derived_from(algorithms.merging.zip_offset)
    def zip_offset(self, *others, offsets, fillvalue=None, longest=False):
        pass

    # ===========
    # Splitting
    # ===========
    @based_on(algorithms.splitting.distribute)
    @with_rich_subiterators(in_tuple=True)
    def distribute(self, n):
        pass

    @based_on(algorithms.splitting.partition)
    @with_rich_subiterators(in_tuple=True)
    def partition(self, predicate):
        pass

    @tuple_wise_version_of(partition)
    def partition_t(self, predicate):
        pass

    @based_on(algorithms.splitting.split_after)
    @with_rich_subiterators()
    def split_after(self, predicate):
        pass

    @tuple_wise_version_of(split_after)
    def split_after_t(self, predicate):
        pass

    @based_on(algorithms.splitting.split_at)
    @with_rich_subiterators()
    def split_at(self, predicate):
        pass

    @tuple_wise_version_of(split_at)
    def split_at_t(self, predicate):
        pass

    @based_on(algorithms.splitting.split_before)
    @with_rich_subiterators()
    def split_before(self, predicate):
        pass

    @tuple_wise_version_of(split_before)
    def split_before_t(self, predicate):
        pass

    @based_on(algorithms.splitting.unzip)
    @with_rich_subiterators(in_tuple=True)
    def unzip(self, arity=2):
        pass

    # ===========
    # (Un)Merging
    # ===========
    @derived_from(algorithms.extra.cartesian_product)
    def cartesian_product(self, *others, repeat=1):
        pass

    # =================
    # Flow manipulation
    # =================
    def find(self, predicate):
        anti_predicate = lambda item: not predicate(item)
        return self.drop_while(anti_predicate).next()

    @tuple_wise_version_of(find)
    def find_t(self, predicate):
        pass

    def first(self):
        return self.next()

    def last(self):
        return self.take_last(1).next()

    @derived_from(algorithms.searching.locate)
    def locate(self, predicate, *, count_from=0):
        pass

    @tuple_wise_version_of(locate)
    def locate_t(self, predicate, *, count_from=0):
        pass

    def nth(self, index):
        '''
        Returns `iter2.option.Some2` with `index`-item or `iter2.option.None2` if it doesn't exist.

        :param index:
        :return: iter2.option.Option2
        '''
        return Iterator2(itertools_islice(self.raw(), index, index + 1)).next()

    @based_on(algorithms.searching.position)
    def position(self, predicate, *, count_from=0):
        # Note: `algorithms.searching.position` returns number, `base_on` places it into `self._iterator`
        idx: int = self._iterator
        return None2 if idx < 0 else Some2(idx)

    @tuple_wise_version_of(position)
    def position_t(self, predicate, *, count_from=0):
        pass

    def sort(self, *, key=None, reverse=False):
        '''
        Sorts items from iterator with builtin `sorted`.

        :param key:
        :param reverse:
        :return:
        '''
        return Iterator2(
            sorted(self._iterator, key=key, reverse=reverse)
        )

    def sort_t(self, *, key=None, reverse=False):
        '''Tuple-wise version of `sort_t`'''
        adapter_key = key and tuple_wise(key)
        return self.sort(key=adapter_key, reverse=reverse)

    def unique(self):
        '''
        Removes equal items from iterator by means of `frozenset`. Order presuming is not guaranteed.

        :return:
        '''
        return Iterator2(frozenset(self.raw()))

    # =============
    # Materializing
    # =============
    def collect(self, factory=tuple):
        return factory(self.raw())

    def to_dict(self):
        return dict(self.raw())

    def to_frozenset(self):
        return frozenset(self.raw())

    def to_list(self):
        return list(self.raw())

    def to_set(self):
        return set(self.raw())

    def to_tuple(self):
        return tuple(self.raw())

    def t(self):
        return tuple(self.raw())

    # ===========
    # Duplication
    # ===========
    def copy(self):
        self._iterator, it_copy = itertools_tee(self._iterator)  # implicit move semantics
        return Iterator2(it_copy)

    def tee(self, n=2):
        copies = itertools_tee(self.raw(), n)
        return tuple(map(Iterator2, copies))

    # =======
    # Folding
    # =======
    def apply(self, func):
        '''
        Uses iterator as an argument for `func`.

        :param func:
        :return:
        '''
        return func(self.raw())

    @derived_from(algorithms.folding.count, wrap_into_iterator=False)
    def count(self):
        pass

    @derived_from(algorithms.folding.fold, wrap_into_iterator=False)
    def fold(self, func, *, initial=None):
        pass

    def fold_t(self, func, *, initial=None):
        '''Tuple-wise version of `fold`'''
        adapter_func = lambda st, item: func(st, *item)
        return self.fold(adapter_func, initial=initial)

    @derived_from(algorithms.folding.join, wrap_into_iterator=False)
    def join(self, sep):
        pass

    @derived_from(algorithms.folding.max, wrap_into_iterator=False)
    def max(self, *, default=None, key=None):
        pass

    def max_t(self, *, default=None, key=None):
        adapter_key = tuple_wise(key)
        return self.max(default=default, key=adapter_key)

    @derived_from(algorithms.folding.min, wrap_into_iterator=False)
    def min(self, *, default=None, key=None):
        pass

    def min_t(self, *, default=None, key=None):
        adapter_key = tuple_wise(key)
        return self.min(default=default, key=adapter_key)

    @derived_from(algorithms.folding.minmax, wrap_into_iterator=False)
    def minmax(self, *, default=None, key=None):
        pass

    def minmax_t(self, *, default=None, key=None):
        adapter_key = tuple_wise(key)
        return self.minmax(default=default, key=adapter_key)

    @derived_from(algorithms.folding.product, wrap_into_iterator=False)
    def product(self):
        pass

    @derived_from(algorithms.folding.reduce, wrap_into_iterator=False)
    def reduce(self, func, *, initial=None):
        pass

    @tuple_wise_version_of(reduce)
    def reduce_t(self, func, *, initial=None):
        pass

    @derived_from(algorithms.folding.sum, wrap_into_iterator=False)
    def sum(self):
        pass

    # ======================
    # Lookahead and lookback
    # ======================
    def spy(self, n=1, *, allow_partial=False):
        if not isinstance(self._iterator, SpyIterator):
            self._iterator = SpyIterator(self._iterator)

        ok, items = self._iterator.spy(n, allow_partial=allow_partial)
        if ok:
            return Some2(items)
        else:
            return None2

