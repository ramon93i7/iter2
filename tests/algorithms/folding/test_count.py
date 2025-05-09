import typing as tp
import hypothesis as hyp

from ... import _hypothesis_strategies as st

from iter2._internal.algorithms.plain.folding._count_items import (
    count_items_by_summing_ones,
    count_items_via_deque_consuming,
)


# ---

@hyp.given(
    items=st.lists(st.none(), max_size=10),
)
def test_count_items_equivalency(
    items: tp.List[None],
):
    assert (
        len(items)
        ==
        count_items_by_summing_ones(items)
        ==
        count_items_via_deque_consuming(items)
    )
