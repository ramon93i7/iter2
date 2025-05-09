import typing as tp


class FailingIterator(tp.Iterator[tp.Never]):
    def __iter__(self):
        return self

    def __next__(self):
        raise Exception('Tried to advance an always failing iterator')
