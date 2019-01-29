import itertools
import operator
import functools

from .iterators.iterator2 import Iterator2

from .utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup exports


# Aliases
builtin_range = range
builtin_map = map

itertools_chain = itertools.chain
itertools_count = itertools.count
itertools_cycle = itertools.cycle
itertools_repeat = itertools.repeat
itertools_takewhile = itertools.takewhile

operator_gt = operator.gt
operator_lt = operator.lt
functools_partial = functools.partial


@export_from_module
def count_from(start=0, *, step=1):
    return Iterator2(itertools_count(start, step))


@export_from_module
def cycle(iterable):
    return Iterator2(itertools_cycle(iterable))


@export_from_module
def empty():
    return Iterator2(())


@export_from_module
def from_args(*items):
    return Iterator2(items)


@export_from_module
def iterate(obj, func):
    return Iterator2(itertools_chain((obj,), itertools_repeat(func))).accumulate(lambda st, f: f(st))


@export_from_module
def numeric_range(*args):
    argc = len(args)
    if argc == 1:
        stop, = args
        start = type(stop)(0)
        step = 1
    elif argc == 2:
        start, stop = args
        step = 1
    elif argc == 3:
        start, stop, step = args
    else:
        err_msg = 'numeric_range takes at most 3 arguments, got {}'
        raise TypeError(err_msg.format(argc))

    values = (start + (step * n) for n in itertools_count())
    if step > 0:
        return Iterator2(itertools_takewhile(functools_partial(operator_gt, stop), values))
    elif step < 0:
        return Iterator2(itertools_takewhile(functools_partial(operator_lt, stop), values))
    else:
        raise ValueError('numeric_range arg 3 (`step`) must not be zero')


@export_from_module
def once(obj):
    return Iterator2((obj,))


@export_from_module
def range(*args, **kwargs):
    return Iterator2(builtin_range(*args, **kwargs))


@export_from_module
def repeat(object, times=None):
    if times is None:
        return Iterator2(itertools_repeat(object))
    else:
        return Iterator2(itertools_repeat(object, times))


@export_from_module
def repeat_call(func, times=None):
    return repeat(func, times=times).map(lambda f: f())


@export_from_module
def tabulate(func, start=0):
    return Iterator2(builtin_map(func, itertools_count(start)))
