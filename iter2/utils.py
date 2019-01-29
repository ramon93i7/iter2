import functools
import types


def define_module_exporter():
    all_list = []
    def export(obj):
        all_list.append(obj.__name__)
        return obj
    return export, all_list


def copy_func(fn):
    if type(fn) is not types.FunctionType:
        return functools.wraps(fn)(lambda *args, **kwargs: fn(*args, **kwargs))
    copy = type(lambda: None)(
        fn.__code__,
        fn.__globals__,
        name=fn.__name__,
        argdefs=fn.__defaults__,
        closure=fn.__closure__
    )
    copy = functools.update_wrapper(copy, fn)
    copy.__kwdefaults__ = fn.__kwdefaults__
    return copy


def alias_for(orig_fn):
    def alias_for_orig_func(alias_fn):
        new_fn = functools.wraps(alias_fn)(copy_func(orig_fn))
        docstring_header = alias_fn.__doc__
        if docstring_header is None:
            docstring_header = 'Alias for {orig_qual_name} ({orig_module_name} :: {orig_name}).'.format(
                orig_qual_name=orig_fn.__qualname__,
                orig_module_name=orig_fn.__module__,
                orig_name=orig_fn.__name__
            )
        docstring_footer = orig_fn.__doc__

        if docstring_footer is None:
            new_fn.__doc__ = docstring_header
        else:
            new_fn.__doc__ = '\n'.join((
                docstring_header,
                '',
                '[Original documentation]',
                docstring_footer
            ))
        return new_fn
    return alias_for_orig_func


class Flag(object):
    __slots__ = ('_val',)

    def __init__(self, val=False):
        self._val = val

    def __bool__(self):
        return bool(self._val)

    def set(self):
        self._val = True
        return self

    def clear(self):
        self._val = False
        return self
