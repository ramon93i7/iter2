import typing as tp
import hypothesis as hyp
from .. import _hypothesis_strategies as st

from iter2.op import (
    nth_item,
    first_item,
    second_item,
    third_item,
)


# ---

@hyp.given(
    items=st.lists(
        st.integers(),
        min_size=1,
        max_size=20,
        unique=True,
    ),
)
def test__get_item_operators(
    items: tp.List[int],
):
    special_get_item = (
        first_item,
        second_item,
        third_item,
    )
    for idx in range(len(items)):
        assert (
            nth_item(idx)(items)  # type: ignore - list size is not statically defined
            ==
            items[idx]
        )
        if idx < len(special_get_item):
            assert (
                special_get_item[idx](items)  # type: ignore - list size is not statically defined
                ==
                items[idx]
            )
