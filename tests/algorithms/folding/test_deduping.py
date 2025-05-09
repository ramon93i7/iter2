import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

import random

from iter2.algo import deduplicate_same_consecutive_items


# ---

def test_deduplicate_same_consecutive_items__trully_lazy():
    deduplicate_same_consecutive_items(FailingIterator())


# ---

@hyp.given(
    items=st.lists(
        st.integers(),
        min_size=2,
        unique=True,
    ),
    random=st.randoms(),
)
def test_deduplicate_same_consecutive_items(
    items: tp.List[int],
    random: random.Random,
):
    polyndromed_items = [*items, None, *reversed(items)]

    with_dupes = []
    for item in polyndromed_items:
        for _ in range(random.randint(1, 5)):
            with_dupes.append(item)

    assert (
        polyndromed_items
        ==
        list(deduplicate_same_consecutive_items(with_dupes))
    )
