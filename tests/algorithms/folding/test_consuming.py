import typing as tp
import hypothesis as hyp

from ... import _hypothesis_strategies as st

from iter2._internal.algorithms.plain.folding import consume_iterator


# ---

@hyp.given(
    items=st.lists(st.integers()),
)
def test_consume_iterator(
    items: tp.List[bool],
):
    xs = []
    consume_iterator(
        xs.append(item)
        for item in items
    )
    assert items == xs
