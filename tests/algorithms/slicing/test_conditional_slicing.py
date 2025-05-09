import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

from functools import partial
import operator

from iter2.algo import (
    iterate_through_items_while_true_and_drop_first_false,
    drop_items_while_true_and_iterate_rest,
)


# ---

def test_conditional_slicing_functions_trully_lazy():
    iterate_through_items_while_true_and_drop_first_false(
        FailingIterator(),
        lambda _: True,
    )
    drop_items_while_true_and_iterate_rest(
        FailingIterator(),
        lambda _: True,
    )


# ---

@hyp.given(
    first_set=st.sets(st.integers()),
    last_set=st.sets(st.integers()),
)
def test_iterate_and_drop_first_items_by_predicate_are_correct(
    first_set: tp.Set[int],
    last_set: tp.Set[int],
):
    last_set -= first_set  # forces to have exclusive items

    first_items = list(first_set)
    last_items = list(last_set)
    sequence = first_items + last_items
    is_item_from_first_set = partial(operator.contains, first_set)

    assert (
        first_items
        ==
        list(iterate_through_items_while_true_and_drop_first_false(
            sequence,
            is_item_from_first_set,
        ))
    )

    assert (
        last_items
        ==
        list(drop_items_while_true_and_iterate_rest(
            sequence,
            is_item_from_first_set,
        ))
    )


@hyp.given(
    items=st.lists(st.integers(), min_size=1, max_size=5),
)
def test_iterate_first_items_by_predicate_consumes_first_false_item(
    items: tp.List[int],
):
    is_item_from_first_set = partial(
        operator.contains,
        items[:-1],  # all except last
    )

    it = iter(items)
    list(iterate_through_items_while_true_and_drop_first_false(it, is_item_from_first_set))  # consume

    assert len(list(it)) == 0  # last item aka `first false-item` was already consumed on predicate-check
