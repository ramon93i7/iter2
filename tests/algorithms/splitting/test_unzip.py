import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st

from iter2.algo import unzip_into_lists


# ---

@hyp.given(
    items=st.lists(
        st.lists(
            st.integers(),
            max_size=5,
        ),
        min_size=2,
        max_size=16,
    ),
)
def test_unzip_is_inverse_for_zip(
    items: tp.List[tp.List[int]],
):
    min_len = min(map(len, items))
    same_size_lists = tuple(xs[:min_len] for xs in items)

    assert (
        same_size_lists
        ==
        unzip_into_lists(
            zip(*same_size_lists),  # type: ignore - tuple of size [2, 16] are OK
            arity_hint=len(same_size_lists),  # type: ignore - len is in [2, 16]
        )
    )
