import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st

from iter2.algo import (
    collect_first_items,
    collect_last_items,
)


# ---

@hyp.given(
    first_items=st.lists(st.integers()),
    last_items=st.lists(st.integers()),
)
def test_first_and_last_items_collected_correctly(
    first_items: tp.List[int],
    last_items: tp.List[int],
):
    sequence = [*first_items, ..., *last_items]

    assert (
        first_items
        ==
        list(collect_first_items(
            sequence,
            count=len(first_items),
        ))
    )

    assert (
        last_items
        ==
        list(collect_last_items(
            sequence,
            count=len(last_items),
        ))
    )
