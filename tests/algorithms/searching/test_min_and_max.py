import hypothesis as hyp
from ... import _hypothesis_strategies as st

import random

from iter2.algo import (
    find_min_value,
    find_max_value,
)


# ---

def test_min_and_max_on_empty_sequence_are_nil():
    assert (
        find_min_value((), key=lambda x: x).is_none()
    )

    assert (
        find_max_value((), key=lambda x: x).is_none()
    )


@hyp.given(
    size=st.supported_sizes(
        min_value=1,
        max_value=100,
    ),
    chosen_idx=st.supported_sizes(
        max_value=100,
    ),
    random=st.randoms(),
)
def test_min_is_correct(
    size: int,
    chosen_idx: int,
    random: random.Random,
):
    size = max(size, chosen_idx + 1)
    key_fn = (lambda value: (lambda idx: (
        value if idx == chosen_idx
        else random.randint(1, 9)
    )))

    assert (
        find_min_value(
            range(size),
            key=key_fn(0),
        ).value_or_raise_exception()
        ==
        chosen_idx
    )

    assert (
        find_max_value(
            range(size),
            key=key_fn(10),
        ).value_or_raise_exception()
        ==
        chosen_idx
    )
