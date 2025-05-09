import typing as tp
import hypothesis as hyp

from .. import _hypothesis_strategies as st

from iter2.algo import (
    enumerate_items,
    enumerate_packed_items,
)


# ---

@hyp.given(
    items=st.iterables(st.none()),
    count_from=st.naturals(),
)
def test_enumerate_items(
    items: tp.Iterable[None],
    count_from: int,
):
    valid_idx = count_from
    for idx, _ in enumerate_items(items, count_from=count_from):
        assert valid_idx == idx
        valid_idx += 1


@hyp.given(
    items=st.iterables(
        st.tuples(st.none(), st.none())
    ),
    count_from=st.naturals(),
)
def test_enumerate_packed_items(
    items: tp.Iterable[tp.Tuple[None, None]],
    count_from: int,
):
    valid_idx = count_from
    for idx, _, _ in enumerate_packed_items(items, count_from=count_from):
        assert valid_idx == idx
        valid_idx += 1
