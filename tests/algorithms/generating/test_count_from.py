import hypothesis as hyp
from ... import _hypothesis_strategies as st

from iter2.algo import (
    count_from,

    drop_first_items_and_iterate_rest,
    iterate_through_first_items,
)


# ---

@hyp.given(
    first_value=st.integers(),
    step=st.positive_integers(max_value=100),
    drop_count=st.positive_integers(max_value=10000),
    take_count=st.positive_integers(max_value=100),
)
def test_any_subseq_of_count_from_is_equivalent_to_range(
    first_value: int,
    step: int,
    drop_count: int,
    take_count: int,
):
    range_start = first_value + drop_count * step
    range_finish = range_start + take_count * step + 1

    for count_from_value, range_value in zip(
        iterate_through_first_items(
            drop_first_items_and_iterate_rest(
                count_from(first_value, step=step),
                count=drop_count,
            ),
            count=take_count,
        ),
        range(range_start, range_finish, step),
    ):
        assert count_from_value == range_value
