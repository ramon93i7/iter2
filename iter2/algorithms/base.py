import itertools

from iter2.utils import define_module_exporter


export_from_module, __all__ = define_module_exporter()


# Aliases
itertools__islice = itertools.islice


@export_from_module
def take_now(iterable, number=1, *, collection=tuple):
    '''
    Returns a tuple with at *most* `number` first items from `iterable`.

    :param iterable:
    :param number:
    :return:

    Example:
    >>> take_now(range(1000000000), 3)
    (0, 1, 2)
    '''
    return collection(itertools__islice(iterable, number))

