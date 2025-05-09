import typing as tp
import hypothesis as hyp

import pytest

from .. import _hypothesis_strategies as st

from iter2.option import (
    Option2,
    None2,
    Some2,

    None2UnwrapError,
)

# ---

def fail_on_call(*args, **kwargs):
    raise Exception('fail test was called')


# ---

@hyp.given(
    value=st.integers(min_value=-5, max_value=5)
)
def test_option_correctly_creates_from_optional(
    value: int,
):
    assert None2 == Option2.from_optional(None)
    assert Some2(value) == Option2.from_optional(value)


# ---

@hyp.given(
    opt_value=st.optionals(st.integers(min_value=-5, max_value=5)),
)
def test_option_is_applyable(
    opt_value: tp.Optional[int],
):
    opt2 = Option2.from_optional(opt_value)
    assert repr(opt2) == opt2.apply(repr) == opt2.apply_and_box(repr).value


# ---

@hyp.given(
    value=st.integers(min_value=-5, max_value=5),
)
def test_option_status_predicates(
    value: int,
):
    assert Some2(value).is_some()
    assert not Some2(value).is_none()

    assert not None2.is_some()
    assert None2.is_none()


@hyp.given(
    other_value=st.integers(min_value=-5, max_value=5),
)
def test_none2_unwrapping(
    other_value: int,
):
    with pytest.raises(None2UnwrapError):
        None2.value_or_raise_exception()

    with pytest.raises(None2UnwrapError):
        None2.boxed_value_or_raise_exception()

    assert (
        other_value
        ==
        None2.value_or(other_value)
        ==
        None2.value_or_else(lambda: other_value)
    )


@hyp.given(
    value=st.integers(min_value=-5, max_value=5),
    other_value=st.integers(min_value=-5, max_value=5),
)
def test_some2_unwrapping(
    value: int,
    other_value: int,
):
    assert (
        value
        ==
        Some2(value).value_or_raise_exception()
        ==
        Some2(value).boxed_value_or_raise_exception().value
        ==
        Some2(value).value_or(other_value)
        ==
        Some2(value).boxed_value_or(other_value).value
        ==
        Some2(value).value_or_else(lambda: other_value)
        ==
        Some2(value).boxed_value_or_else(lambda: other_value).value
    )


@hyp.given(
    values=st.tuples(st.integers()),
)
def test_option_is_mappable(
    values: tp.Tuple[int, ...],
):
    assert (
        str(values)
        ==
        Some2(values).map(str).value
    )

    assert (
        str(values)
        ==
        Some2(values).map_unpacked(lambda *args: str(args)).value
    )

    assert (
        None2
        ==
        None2.map(fail_on_call)  # type: ignore - intended use of meaningless
        ==
        None2.map_unpacked(fail_on_call)  # type: ignore - intended use of meaningless
    )


@hyp.given(
    values=st.tuples(st.integers()),
)
def test_option_is_filterable(
    values: tp.Tuple[int, ...],
):
    sum_is_odd = lambda values: sum(values) % 2 == 1

    assert (
        sum_is_odd(values)
        ==
        Some2(values).filter(sum_is_odd).is_some()
        ==
        Some2(values).filter_unpacked(lambda *args: sum_is_odd(args)).is_some()
    )

    assert (
        None2
        ==
        None2.filter(fail_on_call)  # type: ignore - intended use of meaningless
        ==
        None2.filter_unpacked(fail_on_call)  # type: ignore - intended use of meaningless
    )


@hyp.given(
    value=st.one_of(
        st.integers(min_value=-5, max_value=5),
        st.floats(min_value=0.0, max_value=1.0),
    ),
)
def test_option_is_filterable_by_type(
    value: int | float,
):
    def is_int(obj) -> tp.TypeGuard[int]:
        return isinstance(obj, int)

    assert (
        is_int(value)
        ==
        Some2(value).filter_by_type(int).is_some()
        ==
        Some2(value).filter_by_type_predicate(is_int).is_some()
    )

    assert (
        None2
        ==
        None2.filter_by_type(fail_on_call)  # type: ignore - intended use of meaningless
        ==
        None2.filter_by_type_predicate(fail_on_call)  # type: ignore - intended use of meaningless
    )


@hyp.given(
    opt_value=st.optionals(st.integers(min_value=-5, max_value=5)),
    other_value=st.integers(min_value=-5, max_value=5),
)
def test_option_can_be_resolved(
    opt_value: tp.Optional[int],
    other_value: int,
):
    opt2 = Option2.from_optional(opt_value)
    if opt_value is None:
        assert (
            other_value
            ==
            opt2.resolve(fail_on_call, lambda: other_value)
        )
    else:
        inv = lambda x: -x
        assert (
            inv(opt_value)
            ==
            opt2.resolve(inv, fail_on_call)
        )
