import hypothesis as hyp
from .. import _hypothesis_strategies as st

from iter2.op import (
    pipe,
    compose,
)


# ---

@hyp.given(
    value=st.integers(),
)
def test__pipe_and_compose_operator(
    value: int
):
    def add_one(x: int) -> int:
        return x + 1

    def sub_one(x: int) -> int:
        return x - 1

    def inverse(x: int) -> int:
        return -x

    pipe_seq = (
        add_one,
        inverse,
        str,
        int,
        inverse,
        sub_one,
    )
    compose_seq = (
        sub_one,
        inverse,
        int,
        str,
        inverse,
        add_one,
    )  # pipe_seq[::-1]

    assert (
        value
        ==
        pipe(*pipe_seq)(value)
        ==
        compose(*compose_seq)(value)
    )
