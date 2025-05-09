import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

from iter2.algo import (
    cycle_through_items,
    yield_item_repeatedly,
    repeatedly_call_forever,
)


# ---

def test_cycle_through_items__trully_lazy():
    cycle_through_items(FailingIterator())


# ---

@hyp.given(
    items=st.lists(st.integers()),
    number_of_times=st.naturals(max_value=5),
)
def test_cycle_through_items(
    items: tp.List[int],
    number_of_times: int,
):
    assert(
        (items * number_of_times)
        ==
        list(cycle_through_items(
            items,
            number_of_times=number_of_times,
        ))
    )


@hyp.given(
    item=st.integers(),
    number_of_times=st.naturals(max_value=5),
)
def test_yield_item_repeatedly(
    item: int,
    number_of_times: int,
):
    assert(
        ([item] * number_of_times)
        ==
        list(yield_item_repeatedly(
            item,
            number_of_times=number_of_times,
        ))
    )


@hyp.given(
    number_of_times=st.naturals(max_value=100),
)
def test_repeatedly_call_forever(
    number_of_times: int,
):
    acc = [0]
    def _add_one_to_acc():
        acc[0] += 1

    for _, _ in zip(range(number_of_times), repeatedly_call_forever(_add_one_to_acc)):
        ...

    assert number_of_times == acc[0]
