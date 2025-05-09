import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st

import random

from iter2.algo import find_first_occurrence


# ---

@hyp.given(
    positive_items=st.lists(
        st.positive_integers(),
        max_size=10,
    ),
)
def test_first_occurence_of_missing_item_is_nil(
    positive_items: tp.List[int],
):
    assert (
        find_first_occurrence(
            positive_items,
            lambda x: x < 0,
        )
        .is_none()
    )


def test_first_occurrence_on_empty_sequence_is_nil():
    assert (
        find_first_occurrence(
            (),
            lambda _: True,
        )
        .is_none()
    )


@hyp.given(
    size=st.supported_sizes(
        min_value=1,
        max_value=100,
    ),
    count=st.supported_sizes(
        min_value=1,
        max_value=100,
    ),
    random=st.randoms(),
)
def test_first_occurence_is_valid_having_many(
    size: int,
    count: int,
    random: random.Random,
):
    chosen_idxs = {
        random.randint(0, size - 1)
        for _ in range(count)
    }

    assert (
        find_first_occurrence(
            range(size),
            lambda x: x in chosen_idxs,
        ).value_or_raise_exception()
        ==
        min(chosen_idxs)
    )
