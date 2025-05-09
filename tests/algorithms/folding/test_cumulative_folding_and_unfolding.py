import typing as tp
import operator as op
import hypothesis as hyp
from ... import _hypothesis_strategies as st

from iter2.algo import (
    fold_cumulative,
    unfold_cumulative,
)


# ---

@hyp.given(
    items=st.lists(st.positive_integers()),
)
def test_fold_cumulative(
    items: tp.List[int],
):
    items_prefixes_it = fold_cumulative(
        [
            [item]
            for item in items
        ],
        op.concat,
    )

    for idx, items_prefix in zip(range(1, len(items) + 1), items_prefixes_it):
        assert items[:idx] == items_prefix


@hyp.given(
    items=st.lists(st.positive_integers()),
)
def test_unfold_cumulative_as_opposite_to_fold_cumulative(
    items: tp.List[int],
):
    assert (
        items
        ==
        list(unfold_cumulative(
            fold_cumulative(
                items,
                op.add,
            ),
            op.sub,
        ))
    )
