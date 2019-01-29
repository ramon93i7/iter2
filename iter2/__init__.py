from .iterators.iterator2 import Iterator2
from . import option
from . import sequence_builders
from . import wrapped_algorithms

from iter2.utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()  # setup exports


@export_from_module
def iter2(*args):
    return Iterator2(*args)


# Populate option
iter2.some = option.Some2
iter2.none = option.None2


# Populate sequence builders
iter2.sequence_builders = sequence_builders
iter2.count_from = sequence_builders.count_from
iter2.cycle = sequence_builders.cycle
iter2.empty = sequence_builders.empty
iter2.from_args = sequence_builders.from_args
iter2.of = iter2.from_args
iter2.iterate = sequence_builders.iterate
iter2.numeric_range = sequence_builders.numeric_range
iter2.once = sequence_builders.once
iter2.range = sequence_builders.range
iter2.repeat = sequence_builders.repeat
iter2.repeat_call = sequence_builders.repeat_call
iter2.tabulate = sequence_builders.tabulate


# Populate wrapped algorithms
iter2.cartesian_product = wrapped_algorithms.castesian_product
iter2.sort_together = wrapped_algorithms.sort_together
iter2.unique_to_each = wrapped_algorithms.unique_to_each
iter2.chain = wrapped_algorithms.chain
iter2.chain_from_iterable = wrapped_algorithms.chain_from_iterable
iter2.interleave = wrapped_algorithms.interleave
iter2.interleave_shortest = wrapped_algorithms.interleave_shortest
iter2.roundrobin = wrapped_algorithms.roundrobin
iter2.zip = wrapped_algorithms.zip
iter2.zip_longest = wrapped_algorithms.zip_longest
iter2.zip_offset = wrapped_algorithms.zip_offset

