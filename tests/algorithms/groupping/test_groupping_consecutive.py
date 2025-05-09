import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

import random

import itertools

from iter2.algo import (
    group_consecutive_values_with_same_computable_key,
    group_consecutive_values_by_key,
)


# ---

def test_group_consecutive_functions_are_trully_lazy():
    group_consecutive_values_with_same_computable_key(
        FailingIterator(),
        key_fn=lambda x: x,
    )
    group_consecutive_values_by_key(FailingIterator())


# ---

@hyp.given(
    items=st.lists(
        st.positive_integers(),
        unique=True,
    ),
    random=st.randoms(),
)
def test_group_consecutive_functions_are_eqivalent_to_itertools_groupby(
    items: tp.List[int],
    random: random.Random,
):
    polyndromed_items = [*items, -1, *reversed(items)] if len(items) > 0 else []

    with_dupes = []
    for item in polyndromed_items:
        for _ in range(random.randint(1, 5)):
            with_dupes.append(item)

    computable_groups_it = group_consecutive_values_with_same_computable_key(
        with_dupes,
        key_fn=_classify_neg_odd_even,
    )

    key_value_groups_it = group_consecutive_values_by_key(
        (_classify_neg_odd_even(item), item)
        for item in with_dupes
    )

    valid_groups_it = itertools.groupby(
        with_dupes,
        key=_classify_neg_odd_even,
    )

    for (comp_key, comp_group), (given_key, given_group), (valid_key, valid_group) in zip(
        computable_groups_it,
        key_value_groups_it,
        valid_groups_it,
    ):
        assert comp_key == given_key == valid_key
        for comp_item, given_item, valid_item in zip(comp_group, given_group, valid_group):
            assert comp_item == given_item == valid_item


# ---

def _classify_neg_odd_even(value) -> int:
    if value < 0:
        return 0
    elif value % 2 == 1:
        return 1
    else:
        return -1
