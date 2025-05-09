import typing as tp
import hypothesis as hyp

from ... import _hypothesis_strategies as st

from itertools import product

from iter2.algo import cartesian_product


# ---

@hyp.given(
    items1=st.lists(st.integers()),
    items2=st.lists(st.integers()),
)
def test_cartesian_product_for_2d_is_equivalent_to_itertools_product(
    items1: tp.List[int],
    items2: tp.List[int],
):
    for pair1, pair2 in zip(
        cartesian_product(items1, items2),
        product(items1, items2),
    ):
        assert pair1 == pair2


@hyp.given(
    items=st.lists(
        st.integers(),
        max_size=16,
    ),
    number_of_times=st.naturals(max_value=5),
)
def test_cartesian_product_on_repeat_is_equivalent_to_itertools_product(
    items: tp.List[int],
    number_of_times: int,
):
    for pair1, pair2 in zip(
        cartesian_product(items, repeat=number_of_times),
        product(items, repeat=number_of_times),
    ):
        assert pair1 == pair2
