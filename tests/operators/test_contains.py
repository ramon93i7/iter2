import hypothesis as hyp
from .. import _hypothesis_strategies as st

from iter2.op import contains


# ---

@hyp.given(
    value=st.integers(),
)
def test__contains_operator(
    value: int,
):
    empty = []
    with_value = [value]

    assert not contains(empty, value)
    assert (
        contains(with_value, value)
        and
        contains(value)(with_value)
    )
