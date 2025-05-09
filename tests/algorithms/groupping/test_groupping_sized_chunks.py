import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
import pytest
from .._failing_iterator import FailingIterator

import sys
import random
import itertools

from iter2.algo import (
    iterate_in_chunks_of_at_most_size,
    iterate_in_chunks_of_exact_size_and_drop_left,
    iterate_in_chunks_of_exact_size_with_padding,
)

from iter2._internal.algorithms.plain.groupping._sized_chunks import (
    _iterate_in_chunks_of_at_most_size__via_islice__without_size_check,
    _iterate_in_chunks_of_at_most_size__via_batched__without_size_check,
)


# ---

def test_iterate_in_chunks_are_trully_lazy():
    iterate_in_chunks_of_at_most_size(
        FailingIterator(),
        max_size=1,
    )
    iterate_in_chunks_of_exact_size_and_drop_left(
        FailingIterator(),
        size=1,
    )
    # ---
    iterate_in_chunks_of_exact_size_with_padding(
        FailingIterator(),
        size=1,
    )
    iterate_in_chunks_of_exact_size_with_padding(
        FailingIterator(),
        size=1,
        fill_value=None,
    )
    iterate_in_chunks_of_exact_size_with_padding(
        FailingIterator(),
        size=1,
        fill_value_fn=lambda: None,
    )


# ---

_T = tp.TypeVar('_T')


@st.original.composite
def _sequence_of_sequences_of_exact_size(
    draw: st.original.DrawFn,
    *,
    item_strategy: st.original.SearchStrategy[_T],
    min_len: int = 0,
    max_len: tp.Optional[int] = None,
    min_chunk_size: int = 1,
    max_chunk_size: int = sys.maxsize,
) -> tp.Tuple[int, tp.Sequence[tp.Sequence[_T]]]:
    chunk_size = draw(st.supported_sizes(
        min_value=min_chunk_size,
        max_value=max_chunk_size,
    ))
    seq_of_seq = draw(st.lists(
        st.lists(
            item_strategy,
            min_size=chunk_size,
            max_size=chunk_size,
        ),
        min_size=min_len,
        max_size=max_len,
    ))
    return chunk_size, seq_of_seq


# ---

def test_group_in_chunks_fails_on_zero_sized_chunk_during_iterator_initialization():
    EMPTY_LIST = []
    ZERO = 0

    with pytest.raises(Exception):
        iterate_in_chunks_of_at_most_size(EMPTY_LIST, max_size=ZERO)

    with pytest.raises(Exception):
        iterate_in_chunks_of_exact_size_and_drop_left(EMPTY_LIST, size=ZERO)

    with pytest.raises(Exception):
        iterate_in_chunks_of_exact_size_with_padding(EMPTY_LIST, size=ZERO)


@hyp.given(
    chunk_size = st.supported_sizes(
        min_value=1,  # already have special test for chunk_size == 0
    ),
)
def test_group_in_chunks_of_empty_stream(chunk_size: int):
    empty_list = []
    assert (
        empty_list
        ==
        list(iterate_in_chunks_of_at_most_size(empty_list, max_size=chunk_size))
        ==
        list(iterate_in_chunks_of_exact_size_and_drop_left(empty_list, size=chunk_size))
        ==
        list(iterate_in_chunks_of_exact_size_with_padding(empty_list, size=chunk_size))
    )


# ---

@hyp.given(
    chunk_size_and_seq_of_seqs=_sequence_of_sequences_of_exact_size(
        item_strategy=st.integers(),
        min_len=1,  # already have special test for empty sequences
        max_len=10,
        min_chunk_size=1,  # already have special test for chunk_size == 0
        max_chunk_size=10,
    )
)
def test_iterate_in_chunks_of_at_most_size(
    chunk_size_and_seq_of_seqs: tp.Tuple[int, tp.Sequence[tp.Sequence[int]]],
):
    chunk_size, seq_of_seqs = chunk_size_and_seq_of_seqs

    chunks_it = iterate_in_chunks_of_at_most_size(
        itertools.chain.from_iterable(seq_of_seqs),
        max_size=chunk_size,
    )

    for chunk, valid_chunk in itertools.zip_longest(chunks_it, seq_of_seqs):
        assert chunk == tuple(valid_chunk)


@hyp.given(
    items=st.lists(
        st.integers(),
        max_size=10,
    ),
    chunk_size=st.supported_sizes(
        min_value=1,
        max_value=10,
    ),
)
def test_iterate_in_chunks_of_at_most_size__equivalence_of_two_implementations(
    items: tp.List[int],
    chunk_size: int,
):
    assert (
        list(_iterate_in_chunks_of_at_most_size__via_batched__without_size_check(items, max_size=chunk_size))
        ==
        list(_iterate_in_chunks_of_at_most_size__via_islice__without_size_check(items, max_size=chunk_size))
    )

# ---

@hyp.given(
    chunk_size_and_seq_of_seqs=_sequence_of_sequences_of_exact_size(
        item_strategy=st.integers(),
        min_len=1,  # already have special test for empty sequences
        max_len=10,
        min_chunk_size=2,  # minimal chunk size that can be partial
        max_chunk_size=10,
    ),
    random=st.randoms(),
)
def test_iterate_in_chunks_of_exact_size(
    chunk_size_and_seq_of_seqs: tp.Tuple[int, tp.Sequence[tp.Sequence[int]]],
    random: random.Random,
):
    chunk_size, seq_of_seqs = chunk_size_and_seq_of_seqs

    *head_seqs, last_subseq = seq_of_seqs
    split_point = random.randint(1, len(last_subseq) - 1)
    partial_last_subseq = last_subseq[:split_point]
    partial_seq_of_seqs = [*head_seqs, partial_last_subseq]

    # ---

    exact_and_drop_left_it = iterate_in_chunks_of_exact_size_and_drop_left(
        itertools.chain.from_iterable(partial_seq_of_seqs),
        size=chunk_size,
    )

    for chunk, valid_chunk in itertools.zip_longest(exact_and_drop_left_it, head_seqs):
        assert chunk == tuple(valid_chunk)

    # ---

    partial_last_subseq_none_padded = (
        *partial_last_subseq,
        *([None] * (chunk_size - split_point))
    )

    exact_with_padding_default_it = iterate_in_chunks_of_exact_size_with_padding(
        itertools.chain.from_iterable(partial_seq_of_seqs),
        size=chunk_size,
    )

    for chunk, valid_chunk in itertools.zip_longest(
        exact_with_padding_default_it,
        itertools.chain(head_seqs, (partial_last_subseq_none_padded,)),
    ):
        assert chunk == tuple(valid_chunk)

    # ---

    PADDING_ITEM = object()  # unique

    partial_last_subseq_custom_padded = (
        *partial_last_subseq,
        *([PADDING_ITEM] * (chunk_size - split_point))
    )

    exact_with_padding_custom_it = iterate_in_chunks_of_exact_size_with_padding(
        itertools.chain.from_iterable(partial_seq_of_seqs),
        size=chunk_size,
        fill_value=PADDING_ITEM,
    )

    for chunk, valid_chunk in itertools.zip_longest(
        exact_with_padding_custom_it,
        itertools.chain(head_seqs, (partial_last_subseq_custom_padded,)),
    ):
        assert chunk == tuple(valid_chunk)


    # ---

    PADDING_ITEMS = tuple(
        random.randint(1, 10)
        for _ in range((chunk_size - split_point))
    )

    partial_last_subseq_lazy_custom_padded = (
        *partial_last_subseq,
        *PADDING_ITEMS,
    )

    next_padding_item = iter(PADDING_ITEMS).__next__

    exact_with_lazy_padding_custom_it = iterate_in_chunks_of_exact_size_with_padding(
        itertools.chain.from_iterable(partial_seq_of_seqs),
        size=chunk_size,
        fill_value_fn=next_padding_item,
    )

    for chunk, valid_chunk in itertools.zip_longest(
        exact_with_lazy_padding_custom_it,
        itertools.chain(head_seqs, (partial_last_subseq_lazy_custom_padded,)),
    ):
        assert chunk == tuple(valid_chunk)
