from abc import ABC, abstractmethod
# from iter2.iterators.iterator2 import Iterator2


class Option2(ABC):
    def __getattr__(self, item):
        return getattr(iter(self), item)

    @abstractmethod
    def __bool__(self):
        pass

    @abstractmethod
    def expect(self, exception_type, *ex_args, **ex_kwargs):
        pass

    @abstractmethod
    def is_some(self):
        pass

    @abstractmethod
    def is_none(self):
        pass

    @abstractmethod
    def unwrap(self):
        pass

    @abstractmethod
    def unwrap_or(self, default):
        pass

    @abstractmethod
    def unwrap_or_else(self, default_func):
        pass

    @abstractmethod
    def map(self, func):
        pass

    @abstractmethod
    def map_or(self, default, func):
        pass

    @abstractmethod
    def map_or_else(self, default_func, func):
        pass

    @abstractmethod
    def __and__(self, other):
        pass

    def and_(self, other):
        return self & other

    @abstractmethod
    def and_then(self, func):
        pass

    @abstractmethod
    def filter(self, predicate):
        pass

    @abstractmethod
    def __or__(self, other):
        pass

    def or_(self, other):
        return self | other

    @abstractmethod
    def or_else(self, func):
        pass

    @abstractmethod
    def __xor__(self, other):
        pass

    def xor(self, other):
        return self ^ other


class None2Type(Option2):
    def __repr__(self):
        return '.'.join((self.__module__ , 'None2'))

    def __iter__(self):
        return iter(())

    def __bool__(self):
        return False

    def is_some(self):
        return False

    def is_none(self):
        return True

    def expect(self, exception_type, *ex_args, **ex_kwargs):
        raise exception_type(*ex_args, **ex_kwargs)

    def unwrap(self):
        # TODO: think about better exception type
        raise RuntimeError('Error unwrapping None')

    def unwrap_or(self, default):
        return default

    def unwrap_or_else(self, default_func):
        return default_func()

    def map(self, func):
        return self

    def map_or(self, default, func):
        return default

    def map_or_else(self, default_func, func):
        return default_func()

    def filter(self, predicate):
        return self

    def __and__(self, other):
        return self

    def and_then(self, func):
        return self

    def __or__(self, other):
        return other

    def or_else(self, func):
        return func()

    def __xor__(self, other):
        if other.is_some():
            return other
        else:
            return self


None2 = None2Type()  # Only one instance


class Some2(Option2):
    __slots__ = ('_value',)

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return ''.join(('.'.join((self.__module__, 'Some2')), '(', repr(self._value), ')'))

    def __iter__(self):
        # return Iterator2((self._value,))
        yield self._value

    def __bool__(self):
        return True

    def is_some(self):
        return True

    def is_none(self):
        return False

    def expect(self, exception_type, *ex_args, **ex_kwargs):
        return self._value

    def unwrap(self):
        return self._value

    def unwrap_or(self, default):
        return self._value

    def unwrap_or_else(self, default_func):
        return self._value

    def map(self, func):
        return Some2(func(self._value))

    def map_or(self, default, func):
        return func(self._value)

    def map_or_else(self, default_func, func):
        return func(self._value)

    def filter(self, predicate):
        if predicate(self._value) is True:
            return Some2(self._value)
        else:
            return None2

    def __and__(self, other):
        return other

    def and_then(self, func):
        return func()

    def __or__(self, other):
        return self

    def or_else(self, func):
        return self

    def __xor__(self, other):
        if other.is_none():
            return self
        else:
            return None2