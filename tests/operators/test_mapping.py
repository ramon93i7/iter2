import typing as tp
import hypothesis as hyp
from .. import _hypothesis_strategies as st

from iter2.op import (
    mapping_keys,
    mapping_values,
    mapping_items,
)


# ---

@hyp.given(
    pairs=st.lists(
        st.tuples(
            st.integers(),
            st.integers(),
        ),
        max_size=10,
    ),
)
def test__mapping_operators(
    pairs: tp.List[tp.Tuple[int, int]],
):
    mapping = dict(pairs)

    assert (
        list(mapping_keys(mapping))
        ==
        list(mapping.keys())
    )

    assert (
        list(mapping_values(mapping))
        ==
        list(mapping.values())
    )

    assert (
        list(mapping_items(mapping))
        ==
        list(mapping.items())
    )
