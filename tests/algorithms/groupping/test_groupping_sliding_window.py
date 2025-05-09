import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

import pytest

from iter2.algo import (
    iterate_pairwise,
    iterate_with_sliding_window_of_at_most_size,
    iterate_with_sliding_window_of_exact_size_with_padding,
)


# ---

_MAX_CHUNK_SIZE_FOR_TESTS = 10


# ---

def test_iterate_with_sliding_window_doesnt_advance_iterator_on_initialization():
    iterate_with_sliding_window_of_at_most_size(
        FailingIterator()
    )
    iterate_with_sliding_window_of_exact_size_with_padding(
        FailingIterator(),
        fill_value=None,
    )
    iterate_pairwise(FailingIterator(), fill_value=None)


# ---

@hyp.given(
    chunk_size=st.integers(
        min_value=0,
        max_value=_MAX_CHUNK_SIZE_FOR_TESTS,
    ),
    step=st.integers(
        min_value=0,
        max_value=_MAX_CHUNK_SIZE_FOR_TESTS,
    ),
)
def test_iterate_with_sliding_window_fails_on_invalid_size_or_step_during_iterator_initialization(
    chunk_size: int,
    step: int,
):
    if not (
        chunk_size >= 1  # non-zero
        and
        step >= 1  # non-zero
        and
        step < chunk_size  # with overlap
    ):
        NON_IMPORTANT_EMPTY_LIST = []
        with pytest.raises(Exception):
            iterate_with_sliding_window_of_at_most_size(
                NON_IMPORTANT_EMPTY_LIST,
                size=chunk_size,
                step=step,
            )

        with pytest.raises(Exception):
            iterate_with_sliding_window_of_exact_size_with_padding(
                NON_IMPORTANT_EMPTY_LIST,
                size=chunk_size,
                step=step,
                fill_value=None,
            )


@hyp.given(
    chunk_size=st.positive_integers(
        min_value=2,  # is minimal OK value for window size
        max_value=_MAX_CHUNK_SIZE_FOR_TESTS,
    ),
)
def test_iterate_with_sliding_window_of_empty_stream_must_be_empty(chunk_size: int):
    empty_list = []
    assert (
        empty_list
        ==
        list(iterate_with_sliding_window_of_at_most_size(
            empty_list, size=chunk_size
        ))
        ==
        list(iterate_with_sliding_window_of_exact_size_with_padding(
            empty_list, size=chunk_size, fill_value=None,
        ))
        ==
        list(iterate_pairwise(empty_list, fill_value=None))
    )


# ---

@hyp.given(
    items=st.lists(
        st.integers(),
        min_size=1,
    ),
)
def test_iterate_with_sliding_window_pairwise_is_special_case_of_exact_size_with_padding(
    items: tp.List[int],
):
    sentinel = object()
    assert (
        list(iterate_pairwise(items, fill_value=sentinel))
        ==
        list(iterate_with_sliding_window_of_exact_size_with_padding(
            items, size=2, step=1, fill_value=sentinel,
        ))
    )


# ---

@st.original.composite
def _valid_sliding_window_size_and_step(
    draw: st.original.DrawFn,
) -> tp.Tuple[int, int]:
    size = draw(st.positive_integers(
        min_value=2,
        max_value=100,
    ))
    step = draw(st.positive_integers(
        min_value=1,
        max_value=size - 1,
    ))
    return size, step


# ---

@hyp.given(
    items=st.lists(
        st.integers(),
        min_size=1,
    ),
    size_and_step=_valid_sliding_window_size_and_step(),
)
def test_iterate_with_sliding_window_exact_size_is_at_most_size_but_with_padding(
    items: tp.List[int],
    size_and_step: tp.Tuple[int, int],
):
    size, step = size_and_step
    sentinel = object()

    *at_most_main, at_most_last = list(iterate_with_sliding_window_of_at_most_size(
        items, size=size, step=step,
    ))

    *exact_main, exact_last = list(iterate_with_sliding_window_of_exact_size_with_padding(
        items, size=size, step=step, fill_value=sentinel,
    ))

    # ---

    # 1. all chunks are the same except the last
    assert at_most_main == exact_main

    # 2. last chunks are the same excluding padding with sentinel
    at_most_last_len = len(at_most_last)
    exact_last_items, exact_last_sentinels = exact_last[:at_most_last_len], exact_last[at_most_last_len:]
    assert at_most_last == exact_last_items
    assert exact_last_sentinels == ((sentinel,) * (size - at_most_last_len))


# ---

@hyp.given(
    items=st.lists(
        st.integers(),
        min_size=1,
    ),
    size_and_step=_valid_sliding_window_size_and_step(),
)
def test_iterate_with_sliding_window_at_most_size_is_correct(
    items: tp.List[int],
    size_and_step: tp.Tuple[int, int],
):
    size, step = size_and_step

    *at_most_main, at_most_last = list(iterate_with_sliding_window_of_at_most_size(
        items, size=size, step=step,
    ))

    # ---

    for idx, chunk in enumerate(at_most_main):
        from_idx = idx * step
        to_idx = from_idx + size
        assert (
            chunk
            ==
            tuple(items[from_idx:to_idx])
        )

    assert (
        at_most_last
        ==
        tuple(items[len(at_most_main) * step:])
    )
