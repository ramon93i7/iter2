import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

from iter2.algo import (
    iterate_sequentially_through,
    flatten_iterable,
)


# ---

def test_chaining_are_trully_lazy():
    iterate_sequentially_through(
        FailingIterator(),
        FailingIterator(),
    )
    flatten_iterable(
        FailingIterator(),
    )


# ---

@hyp.given(
    sequences=st.lists(
        st.lists(
            st.integers(),
            max_size=10,
        ),
        max_size=10,
    ),
)
def test_chaining(
    sequences: tp.List[tp.List[int]],
):
    answer = []
    for xs in sequences:
        answer.extend(xs)

    assert (
        answer
        ==
        list(iterate_sequentially_through(
            *map(iter, sequences)
        ))
        ==
        list(flatten_iterable(
            map(iter, sequences)
        ))
    )
