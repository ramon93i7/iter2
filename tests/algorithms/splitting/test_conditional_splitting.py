import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st

from functools import partial
import operator

from iter2.algo import (
    group_and_collect_values_globally_with_same_computable_key,
    split_by_condition,
)


# ---

@hyp.given(
    first_set=st.sets(st.integers()),
    last_set=st.sets(st.integers()),
)
def test_conditional_splitting_is_groupping_by_predicate_as_key(
    first_set: tp.Set[int],
    last_set: tp.Set[int],
):
    last_set -= first_set  # forces to have exclusive items

    first_items = list(first_set)
    last_items = list(last_set)
    sequence = first_items + last_items
    is_item_from_first_set = partial(operator.contains, first_set)

    # ---

    groupping_result = group_and_collect_values_globally_with_same_computable_key(
        sequence,
        key_fn=is_item_from_first_set,
    )
    answer = (
        groupping_result.get(True, []),
        groupping_result.get(False, []),
    )

    # ---

    assert (
        answer
        ==
        split_by_condition(sequence, is_item_from_first_set)
    )
