import hypothesis as hyp
from .. import _hypothesis_strategies as st

from iter2.op import (
    equals,
    greater,
    greater_or_equals,
    lesser,
    lesser_or_equals,
)


# ---

@hyp.given(
    value=st.integers(),
)
def test__comparison_operators(
    value: int,
):
    same = value
    bigger = value + 1
    smaller = value - 1

    assert (
        equals(same, value)
        and
        equals(value)(same)
    )

    assert (
        greater(bigger, value)
        and
        greater(value)(bigger)
    )

    assert (
        greater_or_equals(bigger, value)
        and
        greater_or_equals(value)(bigger)
        and
        greater_or_equals(same, value)
        and
        greater_or_equals(value)(same)
    )

    assert (
        lesser(smaller, value)
        and
        lesser(value)(smaller)
    )

    assert (
        lesser_or_equals(smaller, value)
        and
        lesser_or_equals(value)(smaller)
        and
        lesser_or_equals(same, value)
        and
        lesser_or_equals(value)(same)
    )
