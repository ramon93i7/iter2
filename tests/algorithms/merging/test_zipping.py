import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

import random
import pytest

from iter2.algo import (
    zip_shortest,
    zip_longest,
    zip_same_size,
)


# ---

def test_zipping__trully_lazy():
    zip_shortest(
        FailingIterator(),
        FailingIterator(),
    )
    zip_longest(
        FailingIterator(),
        FailingIterator(),
    )
    zip_same_size(
        FailingIterator(),
        FailingIterator(),
    )


# ---

@hyp.given(
    sequence_of_pairs=st.lists(
        st.tuples(
            st.integers(),
            st.integers(),
        ),
    ),
)
def test_zips_are_valid_and_equal_on_same_length_sequences(
    sequence_of_pairs: tp.List[tp.Tuple[int, int]],
):
    first = [x for x, _ in sequence_of_pairs]
    second = [y for _, y in sequence_of_pairs]
    assert (
        sequence_of_pairs
        ==
        list(zip_shortest(first, second))
        ==
        list(zip_longest(first, second))
        ==
        list(zip_same_size(first, second))
    )


# ---

@hyp.given(
    sequence_of_tripples=st.lists(
        st.tuples(
            st.positive_integers(),
            st.positive_integers(),
            st.positive_integers(),
        ),
    ),
    random=st.randoms(),
)
def test_zip_shortest_shrinks_tails(
    sequence_of_tripples: tp.List[tp.Tuple[int, int, int]],
    random: random.Random,
):
    size = len(sequence_of_tripples)
    first_seq = [x for x, _, __ in sequence_of_tripples]

    second_orig = [y for _, y, __ in sequence_of_tripples]
    second_size = random.randint(0, size)
    second_seq = second_orig[:second_size]

    third_orig = [z for _, __, z in sequence_of_tripples]
    third_size = random.randint(0, size)
    third_seq = third_orig[:third_size]

    answer = [
        (first_seq[i], second_seq[i], third_seq[i])
        for i in range(min(size, second_size, third_size))
    ]

    assert (
        answer
        ==
        list(zip_shortest(
            first_seq,
            second_seq,
            third_seq,
        ))
    )


# ---

@hyp.given(
    sequence_of_tripples=st.lists(
        st.tuples(
            st.positive_integers(),
            st.positive_integers(),
            st.positive_integers(),
        ),
    ),
    longest_position=st.integers(
        min_value=0,
        max_value=2,
    ),
    random=st.randoms(),
)
def test_zip_longest_fills_tails(
    sequence_of_tripples: tp.List[tp.Tuple[int, int, int]],
    longest_position: int,
    random: random.Random,
):
    common_fill_value = object()
    special_fill_values = (object(), object(), object())

    size = len(sequence_of_tripples)

    def shrink_and_fill(orig_seq, common_fill_value, special_fill_value):
        new_size = random.randint(0, size)
        new_seq = orig_seq[:new_size]
        filled_with_common = new_seq + ([common_fill_value] * (size - new_size))
        filled_with_special = new_seq + ([special_fill_value] * (size - new_size))
        return new_seq, filled_with_common, filled_with_special

    seqs = []
    filled_with_common = []
    filled_with_special = []

    for pos in range(3):
        orig = [tpl[pos] for tpl in sequence_of_tripples]
        if pos == longest_position:
            seqs.append(orig)
            filled_with_common.append(orig)
            filled_with_special.append(orig)
        else:
            seq, with_common, with_special = shrink_and_fill(
                orig, common_fill_value, special_fill_values[pos],
            )
            seqs.append(seq)
            filled_with_common.append(with_common)
            filled_with_special.append(with_special)

    answer_with_common = [
        (filled_with_common[0][i], filled_with_common[1][i], filled_with_common[2][i])
        for i in range(size)
    ]

    answer_with_special = [
        (filled_with_special[0][i], filled_with_special[1][i], filled_with_special[2][i])
        for i in range(size)
    ]

    seqs = tp.cast(tp.Tuple[tp.Sequence[int], tp.Sequence[int], tp.Sequence[int]], seqs)

    # ---

    assert (
        answer_with_common
        ==
        list(zip_longest(
            *seqs,
            fill_value=common_fill_value,
        ))
        ==
        list(zip_longest(
            *seqs,
            fill_values=(common_fill_value, common_fill_value, common_fill_value),
        ))
    )

    assert (
        answer_with_special
        ==
        list(zip_longest(
            *seqs,
            fill_values=special_fill_values,
        ))
    )


# ---

@hyp.given(
    sequence=st.lists(
        st.integers(),
        min_size=1,  # has at least one item
    ),
)
def test_zip_same_size_fails_on_non_same_size_sequences(
    sequence: tp.List[int],
):
    with pytest.raises(ValueError):
        list(zip_same_size(
            sequence,
            sequence[:-1],
        ))
