import typing as tp
import hypothesis as hyp
from .. import _hypothesis_strategies as st

import random

from iter2.algo import (
    filter_items,
    filter_none_items,
    filter_items_by_type_predicate,
    filter_items_by_type,
)


# ---

@hyp.given(
    items1=st.sets(st.integers()),
    raw_items2=st.sets(st.integers()),
    random=st.randoms(),
)
def test_filter_items_really_filters(
    items1: tp.Set[int],
    raw_items2: tp.Set[int],
    random: random.Random,
):
    items2 = raw_items2 - items1

    all_items = [*items1, *items2]
    random.shuffle(all_items)

    contains_in = (lambda ss: (lambda item: (
        item in ss
    )))

    for inversed in (False, True):
        for some_items in (items1, items2):
            for item in filter_items(
                all_items,
                contains_in(some_items),
                inverse=inversed,
            ):
                assert (item not in some_items) is inversed


# ---

@hyp.given(
    items=st.sets(st.integers()),
    other_items=st.sets(st.floats()),
    random=st.randoms(),
)
def test_filtering_items_by_type_is_correct(
    items: tp.Set[int],
    other_items: tp.Set[float],
    random: random.Random,
):
    all_items = [*items, *other_items]
    random.shuffle(all_items)

    def is_int(obj) -> tp.TypeGuard[int]:
        return isinstance(obj, int)

    assert (
        items
        ==
        set(filter_items_by_type_predicate(all_items, is_int))
        ==
        set(filter_items_by_type(all_items, int))
    )


# ---

@hyp.given(
    items=st.lists(st.one_of(st.integers(), st.none())),
)
def test_filter_none_items_as_special_case_of_generic_filter_items(
    items: tp.List[int | None],
):
    assert (
        list(filter_none_items(items))
        ==
        list(filter_items(items, (lambda item: (
            item is not None
        ))))
    )
