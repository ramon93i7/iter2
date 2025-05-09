import typing as tp
import operator as op
import hypothesis as hyp
from ... import _hypothesis_strategies as st

from functools import reduce

from iter2.algo import fold_items


# ---

@hyp.given(
    initial=st.positive_integers(max_value=5),
    items=st.lists(st.positive_integers()),
)
def test_fold_items_via_sum(
    initial: int,
    items: tp.List[int],
):
    assert(
        sum(items) + initial
        ==
        reduce(op.add, items, initial)
        ==
        fold_items(items, initial, op.add)
        ==
        fold_items(items, op.add).value_or(0) + initial
        ==
        fold_items(items, fn=op.add).value_or(0) + initial
        ==
        fold_items(items, initial_fn=lambda: initial, fn=op.add)
    )
