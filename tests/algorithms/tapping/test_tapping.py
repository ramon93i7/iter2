import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

from iter2._internal.algorithms.plain.folding import consume_iterator

from iter2.algo import (
    map_tap_items,
    map_tap_items_periodically,
    map_tap_packed_items,
    map_tap_packed_items_periodically,
)


# ---

def test_tapping_functions_are_trully_lazy():
    it = FailingIterator()
    id = lambda x: x

    map_tap_items(it, id)
    map_tap_packed_items(it, id)


@hyp.given(
    N=st.integers(min_value=1, max_value=10),
)
def test_packed_tapping_functions_are_trully_lazy(
    N: int
):
    it = FailingIterator()
    id = lambda x: x

    map_tap_items_periodically(it, action=id, step_size=N)
    map_tap_packed_items_periodically(it, action=id, step_size=N)


# ---

@hyp.given(
    items=st.lists(
        st.tuples(st.integers(), st.integers()),
        max_size=10,
    ),
)
def test_tapping_functions_are_correct(
    items: tp.List[tp.Tuple[int, int]],
):
    tapped = []
    consume_iterator(
        map_tap_items(items, tapped.append)
    )
    packed_tapped = []
    consume_iterator(
        map_tap_packed_items(items, lambda *args: packed_tapped.append(args))
    )

    assert items == tapped
    assert items == packed_tapped


@hyp.given(
    items=st.lists(
        st.tuples(st.integers(), st.integers()),
        max_size=10,
    ),
    step_size=st.integers(min_value=1, max_value=10),
)
def test_tapping_periodically_functions_are_correct(
    items: tp.List[tp.Tuple[int, int]],
    step_size: int,
):
    tapped = []
    consume_iterator(
        map_tap_items_periodically(
            items,
            action=tapped.append,
            step_size=step_size,
        )
    )
    packed_tapped = []
    consume_iterator(
        map_tap_packed_items_periodically(
            items,
            action=(lambda *args: packed_tapped.append(args)),
            step_size=step_size,
        )
    )

    answer = items[::step_size]

    assert answer == tapped
    assert answer == packed_tapped
