import itertools
import collections

itertools_chain = itertools.chain
itertools_islice = itertools.islice
collections_deque = collections.deque


# TODO: refactor this shit
class Result(object):
    __slots__ = ('value',)

    def __init__(self, value=None):  # assumed not used explicitly
        self.value = value

    def __iter__(self):
        yield self.is_ok  # for child classes only
        yield self.value


class Ok(Result):
    is_ok = True
    is_error = False


class Error(Result):
    is_ok = False
    is_error = True

#


class SpyIterator(object):
    __slots__ = ('_iterator', '_spied')

    def __init__(self, iterable):
        self._iterator = iter(iterable)
        self._spied = collections_deque()

    def __iter__(self):
        spied = self._spied
        for _ in range(len(spied)):
            yield spied.popleft()
        yield from self._iterator

    def __next__(self):
        spied = self._spied
        if len(spied) > 0:
            return spied.popleft()
        else:
            return next(self._iterator)

    def raw(self):
        raw_it = itertools_chain(self._spied, self._iterator)
        self.__init__(())
        return raw_it

    def spy(self, n=1, *, allow_partial=False):
        spied = self._spied
        spied_count = len(spied)
        if n > spied_count:
            spied.extend(itertools_islice(self._iterator, n - spied_count))
            if n > len(spied):
                if not allow_partial or n == 1:
                    return Error()
                else:
                    return Ok(tuple(itertools_islice(spied, n)))
        if n == 1:
            return Ok(spied[0])
        else:
            return Ok(tuple(itertools_islice(spied, n)))
